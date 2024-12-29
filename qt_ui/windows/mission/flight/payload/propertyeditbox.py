import re
from typing import Dict, Callable, Union

from PySide6.QtGui import QFocusEvent
from PySide6.QtWidgets import QLineEdit
from dcs.unitpropertydescription import UnitPropertyDescription

from game.ato import Flight
from game.ato.flightmember import FlightMember
from game.radio.datalink import DataLinkKey


class PropertyEditBox(QLineEdit):
    def __init__(
        self,
        flight_member: FlightMember,
        prop: UnitPropertyDescription,
        flight: Flight,
    ) -> None:
        super().__init__()
        self.flight_member = flight_member
        self.prop = prop
        self.flight = flight

        self.setFixedWidth(100)
        self.setText(
            self.flight_member.properties.get(self.prop.identifier, self.prop.default)
        )

        self.textChanged.connect(self.on_value_changed)

        self._datalink_handlers: Dict[
            DataLinkKey,
            Union[Callable[[int, str], str], Callable[[int, str, bool], str]],
        ] = {
            DataLinkKey.LINK16: self._link16_input,
            DataLinkKey.SADL: self._sadl_input,
            DataLinkKey.IDM: self._idm_input,
        }

    @property
    def datalink_type(self) -> DataLinkKey:
        return DataLinkKey.from_aircraft_type(self.flight.unit_type)

    def focusOutEvent(self, e: QFocusEvent) -> None:
        super(PropertyEditBox, self).focusOutEvent(e)
        link_type = self.datalink_type
        if (handler := self._datalink_handlers.get(link_type)) is not None:
            value = handler(0, self.text(), True)
            self.setText(value)

    def on_value_changed(self, value: str) -> None:
        cursor = self.cursorPosition()
        link_type = self.datalink_type
        if (handler := self._datalink_handlers.get(link_type)) is not None:
            value = handler(cursor, value.upper())
        if not value and self.prop.identifier in self.flight_member.properties:
            del self.flight_member.properties[self.prop.identifier]
        else:
            self.flight_member.properties[self.prop.identifier] = value
        self.setText(value)
        self.setCursorPosition(cursor)
        if cursor > len(value):
            self.setCursorPosition(0)

    def _link16_input(self, cursor: int, value: str, focus_lost: bool = False) -> str:
        max_input_length = 5
        if "VoiceCallsign" in self.prop.identifier:
            max_input_length = 2
        value = self.common_link16_sadl_logic(
            cursor, focus_lost, max_input_length, "STN_L16", value
        )
        return value

    def common_link16_sadl_logic(
        self,
        cursor: int,
        focus_lost: bool,
        max_input_length: int,
        identifier: str,
        value: str,
    ) -> str:
        value = value[:max_input_length]
        if not (
            ("Label" in self.prop.identifier and value.isalpha())
            or ("Number" in self.prop.identifier and value.isdigit())
            or (identifier == self.prop.identifier and self._is_octal(value))
        ):
            value = self._restore_from_property(cursor)
        if focus_lost and 2 < max_input_length > len(value):
            # STN_L16 --> prepend with zeroes
            value = "0" * (max_input_length - len(value)) + value
        return value

    def _restore_from_property(self, cursor):
        props = self.flight_member.properties
        value = props.get(self.prop.identifier, "")[: cursor - 1]
        return value

    @staticmethod
    def _is_octal(value: str) -> bool:
        if re.match(r"^[0-7]+$", value):
            return True
        return False

    def _sadl_input(self, cursor: int, value: str, focus_lost: bool = False) -> str:
        max_input_length = 4
        if "VoiceCallsign" in self.prop.identifier:
            max_input_length = 2
        value = self.common_link16_sadl_logic(
            cursor, focus_lost, max_input_length, "SADL_TN", value
        )
        return value

    def _idm_input(self, cursor: int, value: str, _: bool = False) -> str:
        if "TN_IDM_LB" == self.prop.identifier:
            value = value[:2]  # Originator ID
            if len(value) == 1 and not value.isalnum():
                return ""
            elif len(value) == 2 and not self._valid_2char_idm(value):
                value = str(value[0])
        else:
            value = value[:5]  # Ownship CallSign
            if not re.match(r"^[A-Z0-9/*\-+.]{,5}$", value):
                value = self._restore_from_property(cursor)
        return value

    @staticmethod
    def _valid_2char_idm(value: str) -> bool:
        if len(value) != 2:
            return False
        first = value[0]
        second = value[1]
        return (
            first in ["1", "2"]
            and second.isalnum()
            or first == "3"
            and (re.match(r"^[A-I]$", second) or second.isdigit())
        )

    def set_flight_member(self, flight_member: FlightMember) -> None:
        self.flight_member = flight_member
        self.setText(
            self.flight_member.properties.get(self.prop.identifier, self.prop.default)
        )
