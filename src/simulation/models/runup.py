"""
runup.py
"""

from dataclasses import dataclass
import numpy as np


@dataclass(slots=True)
class RunupResult:

    runup_height: np.ndarray

    shoreline_height: np.ndarray

    maximum_runup: float

    average_runup: float

    coastal_length: float