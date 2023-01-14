from typing import Optional

from game.radio.tacan import TacanChannel


class TacanContainer:
    tacan: Optional[TacanChannel] = None
    tcn_name: Optional[str] = None
