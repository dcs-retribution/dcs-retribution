from abc import abstractmethod
from typing import Optional, List


class Callsign:
    name: Optional[str] = None
    nr: Optional[int] = None

    def __init__(self, name: Optional[str], nr: int) -> None:
        self.name = name
        self.nr = nr


class CallsignContainer:
    callsign: Optional[Callsign] = None

    @property
    @abstractmethod
    def available_callsigns(self) -> List[str]:
        ...
