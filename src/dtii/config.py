"""
config.py

Configuration for DTII Engine.
"""

from dataclasses import dataclass


@dataclass
class DTIIConfig:
    """
    Configuration parameters.
    """

    # -------------------------------
    # Feature ranges
    # -------------------------------

    MIN_FEATURE_VALUE: float = 0.0
    MAX_FEATURE_VALUE: float = 1.0

    # -------------------------------
    # DTII thresholds
    # -------------------------------

    VERY_LOW: float = 0.20
    LOW: float = 0.40
    MODERATE: float = 0.60
    HIGH: float = 0.80
    VERY_HIGH: float = 1.00

    # -------------------------------
    # Normalization
    # -------------------------------

    EPSILON: float = 1e-9