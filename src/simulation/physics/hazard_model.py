"""
hazard_model.py

Tsunami hazard estimation.
"""

from __future__ import annotations

import numpy as np


class HazardModel:

    @staticmethod
    def hazard_index(
        wave: np.ndarray,
        inundation: np.ndarray,
        runup: np.ndarray
    ) -> np.ndarray:

        wave = np.asarray(
            wave,
            dtype=float
        )

        inundation = np.asarray(
            inundation,
            dtype=float
        )

        runup = np.asarray(
            runup,
            dtype=float
        )

        score = (
            0.5 * wave +
            0.3 * inundation +
            0.2 * runup
        )

        return np.clip(
            score,
            0.0,
            10.0
        )