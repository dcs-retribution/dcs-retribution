from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from threading import Event, Thread
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from game.debriefing import Debriefing
    from game.sim import MissionSimulation


class PollDebriefingFileThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(
        self,
        callback: Callable[[Debriefing], None],
        mission_sim: MissionSimulation,
    ) -> None:
        super().__init__()
        self._stop_event = Event()
        self.callback = callback
        self.mission_sim = mission_sim

    def stop(self) -> None:
        self._stop_event.set()

    def stopped(self) -> bool:
        return self._stop_event.is_set()

    def run(self) -> None:
        if os.path.isfile("state.json"):
            last_modified = os.path.getmtime("state.json")
        else:
            last_modified = 0
        while not self.stopped():
            try:
                if (
                    os.path.isfile("state.json")
                    and os.path.getmtime("state.json") > last_modified
                ):
                    debriefing = self.mission_sim.debrief_current_state(
                        Path("state.json")
                    )
                    self.callback(debriefing)
                    last_modified = os.path.getmtime("state.json")
                    if debriefing.state_data.mission_ended:
                        break
            except (json.JSONDecodeError, OSError, ValueError, KeyError):
                logging.warning(
                    "Failed to read state.json. Probably attempted read while DCS "
                    "was still writing the file. Will retry in 5 seconds."
                )
            time.sleep(5)
