"""
context.py

Stores current tsunami situation.
"""

from dataclasses import dataclass


@dataclass
class TsunamiContext:

    magnitude: float

    wave_height: float

    bathymetry_depth: float

    coastal_slope: float

    inundation_area: float

    prediction_error: float

    sensor_confidence: float