"""
inundation.py
"""

from dataclasses import dataclass
import numpy as np


@dataclass(slots=True)
class InundationResult:

    flood_depth: np.ndarray

    inundation_mask: np.ndarray

    flooded_area_km2: float

    maximum_depth: float

    mean_depth: float

    def flooded_pixels(self):

        return int(

            self.inundation_mask.sum()

        )