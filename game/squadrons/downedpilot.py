from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, TYPE_CHECKING
from uuid import UUID, uuid4

from dcs.mapping import Point

from game.sidc import (
    Entity,
    SidcDescribable,
    StandardIdentity,
    Status,
    SymbolSet,
)
from game.theater.missiontarget import MissionTarget
from game.theater.player import Player
from game.utils import Distance

if TYPE_CHECKING:
    from game.ato.flighttype import FlightType
    from game.coalition import Coalition
    from game.settings import Settings
    from game.squadrons.pilot import Pilot
    from game.squadrons.squadron import Squadron


# Dismounted individual, "combatant" entity (APP-6 symbol set 27). The specific
# combat-search-and-rescue survivor entity is not modelled by milsymbol, so we use
# the generic combatant which renders as a dismounted individual.
_DOWNED_PILOT_ENTITY = 110100


@dataclass(eq=False)
class DownedPilot(SidcDescribable, MissionTarget):
    """A pilot who ejected/was shot down and is awaiting CSAR rescue on the map.

    Persisted with the save (in ``Coalition.downed_pilots``) so that CSAR becomes a
    campaign-persistent mission type: a downed pilot exists across turns, can be
    targeted by a CSAR package, and expires (goes MIA) on a countdown.

    Implements :class:`MissionTarget` so it can be used directly as a package target
    (no changes to the package builder/fulfiller) and :class:`SidcDescribable` so the
    map layer has a symbol.
    """

    pilot: Pilot
    squadron: Squadron
    _position: Point
    player: Player
    turn_downed: int
    turns_remaining: int
    was_player: bool
    aircraft_name: str
    id: UUID = field(default_factory=uuid4)
    #: Ditched at sea rather than come down on land. Decided once, when the pilot
    #: is created, and persisted: the landmap does not change, and every consumer
    #: needs the same answer.
    in_water: bool = False

    def __post_init__(self) -> None:
        MissionTarget.__init__(self, self.display_name, self._position)

    def __setstate__(self, state: dict[str, object]) -> None:
        # Saves from before water rescues existed put every pilot on land.
        state.setdefault("in_water", False)
        self.__dict__.update(state)

    def cluster(self, radius: Distance) -> list[DownedPilot]:
        """This pilot plus any close enough to be collected on the same lift.

        Always includes self, and always first: the rest of the pipeline treats
        the head of the list as the one the rescue flight is actually planned
        against.
        """
        if radius.meters <= 0:
            return [self]
        return [self] + [
            other
            for other in self.coalition.downed_pilots
            if other is not self
            and other.position.distance_to_point(self.position) <= radius.meters
        ]

    def needs_hover_extraction(self, settings: Settings) -> bool:
        """Whether this pilot must be winched out rather than walked aboard.

        A helicopter cannot land next to a survivor in the water, so they force a
        hover extraction whatever the ``csar_hover_extraction`` setting says.
        """
        return settings.csar_hover_extraction or self.in_water

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DownedPilot):
            return False
        return self.id == other.id

    @property
    def display_name(self) -> str:
        return f"Downed pilot: {self.pilot.name} ({self.aircraft_name})"

    # MissionTarget overrides ------------------------------------------------

    @property
    def position(self) -> Point:
        return self._position

    @position.setter
    def position(self, value: Point) -> None:
        self._position = value

    @property
    def coalition(self) -> Coalition:
        return self.squadron.coalition

    def is_friendly(self, to_player: Player) -> bool:
        return self.player == to_player

    def mission_types(self, for_player: Player) -> Iterator[FlightType]:
        from game.ato.flighttype import FlightType

        # Only the owning coalition can rescue their own downed pilot.
        if not self.is_friendly(for_player):
            return
        yield FlightType.CSAR
        # Escort types so escorts remain plannable for the package.
        yield FlightType.ESCORT
        yield FlightType.SEAD_ESCORT
        yield FlightType.TARCAP

    # SidcDescribable --------------------------------------------------------

    @property
    def standard_identity(self) -> StandardIdentity:
        return (
            StandardIdentity.FRIEND
            if self.player.is_blue
            else StandardIdentity.HOSTILE_FAKER
        )

    @property
    def sidc_status(self) -> Status:
        return Status.PRESENT

    @property
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.DISMOUNTED_INDIVIDUAL, _CombatantEntity.COMBATANT


class _CombatantEntity(Entity):
    COMBATANT = _DOWNED_PILOT_ENTITY
