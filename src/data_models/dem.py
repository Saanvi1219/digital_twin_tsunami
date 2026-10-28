from dataclasses import dataclass
import numpy as np

@dataclass
class DEMData:
    elevation: np.ndarray
    transform: object
    crs: str
    bounds: tuple
    resolution: tuple
    width: int
    height: int