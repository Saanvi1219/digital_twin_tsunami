"""
runup_model.py

Tsunami runup estimation.
"""

from __future__ import annotations

import numpy as np


class RunupModel:

    @staticmethod
    def estimate(
        wave_height: np.ndarray,
        slope: np.ndarray
    ) -> np.ndarray:

        wave_height = np.asarray(
            wave_height,
            dtype=float
        )

        slope = np.asarray(
            slope,
            dtype=float
        )

        slope = np.nan_to_num(
            slope,
            nan=0.0,
            posinf=0.0,
            neginf=0.0
        )

        slope_factor = 1.0 + np.clip(
            slope,
            0.0,
            1.0
        )

        return np.maximum(
            wave_height * slope_factor,
            0.0
        )