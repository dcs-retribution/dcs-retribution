from typing import Optional

from game.radio.RadioFrequencyContainer import RadioFrequencyContainer
from game.radio.radios import RadioFrequency


class Link4Container(RadioFrequencyContainer):
    link4: Optional[RadioFrequency] = None
