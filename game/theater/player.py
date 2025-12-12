from enum import Enum


class Player(Enum):
    NEUTRAL = "Neutral"
    BLUE = "Blue"
    RED = "Red"

    @property
    def is_red(self) -> bool:
        """Returns True if the player is Red."""
        return self == Player.RED

    @property
    def is_blue(self) -> bool:
        """Returns True if the player is Blue."""
        return self == Player.BLUE

    @property
    def is_neutral(self) -> bool:
        """Returns True if the player is Neutral."""
        return self == Player.NEUTRAL

    @property
    def opponent(self) -> "Player":
        """Returns the opponent player."""
        if self.is_blue:
            return Player.RED
        else:
            return Player.BLUE
