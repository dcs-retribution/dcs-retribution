from __future__ import unicode_literals

from game.settings import Settings

# fmt: off
RUNWAY_REPAIR = f"{Settings.automate_runway_repair=}".split("=")[0].split(".")[1]
FRONTLINE = f"{Settings.automate_front_line_reinforcements=}".split("=")[0].split(".")[1]
AIRCRAFT = f"{Settings.automate_aircraft_reinforcements=}".split("=")[0].split(".")[1]
MISSION_LENGTH = f"{Settings.desired_player_mission_duration=}".split("=")[0].split(".")[1]
SUPER_CARRIER = f"{Settings.supercarrier=}".split("=")[0].split(".")[1]
SQN_AC_LIMITS = f"{Settings.enable_squadron_aircraft_limits=}".split("=")[0].split(".")[1]
# fmt: on
