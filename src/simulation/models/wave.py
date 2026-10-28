"""
wave.py

Wave simulation result.
"""

from dataclasses import dataclass
import numpy as np


@dataclass(slots=True)
class WaveResult:

    wave_height: np.ndarray

    travel_time: np.ndarray

    velocity: np.ndarray

    max_height: float

    average_height: float

    propagation_time: float

    def shape(self):

        return self.wave_height.shape

    @property
    def grid_size(self):

        return self.wave_height.shape