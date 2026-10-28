"""
simulation_result.py
"""

from dataclasses import dataclass
from datetime import datetime

from .earthquake import Earthquake
from .wave import WaveResult
from .inundation import InundationResult
from .hazard import HazardResult
from .runup import RunupResult


@dataclass(slots=True)
class SimulationResult:

    earthquake: Earthquake

    wave: WaveResult

    inundation: InundationResult

    hazard: HazardResult

    runup: RunupResult

    execution_time: float

    created_at: datetime

    engine_version: str = "1.0"

    successful: bool = True

    def summary(self):

        return {

            "max_wave":

                self.wave.max_height,

            "flooded_area":

                self.inundation.flooded_area_km2,

            "max_runup":

                self.runup.maximum_runup,

            "highest_risk":

                self.hazard.highest_risk,

            "execution_time":

                self.execution_time

        }