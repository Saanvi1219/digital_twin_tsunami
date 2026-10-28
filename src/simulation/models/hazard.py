"""
hazard.py
"""

from dataclasses import dataclass
import numpy as np


@dataclass(slots=True)
class HazardResult:

    hazard_map: np.ndarray

    risk_score: np.ndarray

    evacuation_time: np.ndarray

    highest_risk: float

    average_risk: float

    def dimensions(self):

        return self.hazard_map.shape