"""
attenuation.py

Tsunami wave attenuation algorithms.
"""

from __future__ import annotations

import numpy as np


class WaveAttenuation:

    @staticmethod
    def linear(
        wave_height: np.ndarray,
        coefficient: float = 0.02
    ) -> np.ndarray:

        coefficient = np.clip(
            coefficient,
            0.0,
            1.0
        )

        return wave_height * (
            1.0 - coefficient
        )

    @staticmethod
    def exponential(
        wave_height: np.ndarray,
        distance: np.ndarray,
        alpha: float = 0.0005
    ) -> np.ndarray:

        return (
            wave_height *
            np.exp(
                -alpha *
                np.asarray(distance)
            )
        )

    @staticmethod
    def logarithmic(
        wave_height: np.ndarray,
        distance: np.ndarray
    ) -> np.ndarray:

        return wave_height / np.log1p(
            np.asarray(distance) + 1.0
        )