from __future__ import annotations

from dataclasses import dataclass, field
from enum import unique, Enum
from typing import Any

from faker import Faker


@dataclass
class PilotRecord:
    missions_flown: int = field(default=0)


@unique
class PilotStatus(Enum):
    Active = "Active"
    OnLeave = "On leave"
    Dead = "Dead"
    #: Ejected/shot down and awaiting CSAR rescue on the map.
    Downed = "Downed"
    #: Rescued by CSAR but temporarily unavailable while recovering.
    Recovering = "Recovering"
    #: A downed pilot who was never rescued in time.
    MissingInAction = "Missing in action"


@dataclass
class Pilot:
    name: str
    player: bool = field(default=False)
    status: PilotStatus = field(default=PilotStatus.Active)
    record: PilotRecord = field(default_factory=PilotRecord)
    #: Number of turns until a Recovering pilot returns to Active. Only meaningful
    #: while status is Recovering.
    turns_until_available: int = field(default=0)

    def __setstate__(self, state: dict[str, Any]) -> None:
        # Older saves predate CSAR and won't have this field.
        if "turns_until_available" not in state:
            state["turns_until_available"] = 0
        self.__dict__.update(state)

    @property
    def alive(self) -> bool:
        return self.status not in (PilotStatus.Dead, PilotStatus.MissingInAction)

    @property
    def on_leave(self) -> bool:
        return self.status is PilotStatus.OnLeave

    @property
    def downed(self) -> bool:
        return self.status is PilotStatus.Downed

    @property
    def recovering(self) -> bool:
        return self.status is PilotStatus.Recovering

    @property
    def missing_in_action(self) -> bool:
        return self.status is PilotStatus.MissingInAction

    def send_on_leave(self) -> None:
        if self.status is not PilotStatus.Active:
            raise RuntimeError("Only active pilots may be sent on leave")
        self.status = PilotStatus.OnLeave

    def return_from_leave(self) -> None:
        if self.status is not PilotStatus.OnLeave:
            raise RuntimeError("Only pilots on leave may be returned from leave")
        self.status = PilotStatus.Active

    def kill(self) -> None:
        self.status = PilotStatus.Dead

    def go_down(self) -> None:
        """Marks the pilot as shot down and awaiting CSAR rescue."""
        self.status = PilotStatus.Downed

    def go_mia(self) -> None:
        """Marks a downed pilot as missing in action (rescue never came)."""
        if self.status is not PilotStatus.Downed:
            raise RuntimeError("Only downed pilots may go missing in action")
        self.status = PilotStatus.MissingInAction

    def begin_recovery(self, turns: int) -> None:
        """Marks a rescued pilot as recovering for the given number of turns.

        A value of zero (or less) returns the pilot to active duty immediately.
        """
        if turns <= 0:
            self.status = PilotStatus.Active
            self.turns_until_available = 0
            return
        self.status = PilotStatus.Recovering
        self.turns_until_available = turns

    def advance_recovery(self) -> None:
        """Advances a recovering pilot's countdown by one turn.

        Returns the pilot to active duty once the countdown reaches zero.
        """
        if self.status is not PilotStatus.Recovering:
            return
        self.turns_until_available -= 1
        if self.turns_until_available <= 0:
            self.turns_until_available = 0
            self.status = PilotStatus.Active

    @classmethod
    def random(cls, faker: Faker) -> Pilot:
        return Pilot(faker.name())
