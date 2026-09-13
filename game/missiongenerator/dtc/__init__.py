"""Native DCS DTC cartridge pre-population.

See :mod:`game.missiongenerator.dtc.cartridge` for the format and
:mod:`game.missiongenerator.dtc.generator` for the generation pass.
"""

from game.missiongenerator.dtc.cartridge import DtcCartridge
from game.missiongenerator.dtc.generator import CARTRIDGE_BUILDERS, DtcGenerator

__all__ = ["CARTRIDGE_BUILDERS", "DtcCartridge", "DtcGenerator"]
