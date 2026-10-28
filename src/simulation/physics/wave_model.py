"""
wave_model.py

Tsunami shallow-water wave calculations.
"""

from __future__ import annotations

import numpy as np

from .constants import GRAVITY, MIN_DEPTH


class WaveModel:

    @staticmethod
    def wave_speed(depth: np.ndarray) -> np.ndarray:

        depth = np.asarray(depth, dtype=float)

        safe_depth = np.maximum(
            depth,
            MIN_DEPTH
        )

        return np.sqrt(
            GRAVITY * safe_depth
        )

    @staticmethod
    def travel_time(
        distance: np.ndarray,
        depth: np.ndarray
    ) -> np.ndarray:

        distance = np.asarray(
            distance,
            dtype=float
        )

        speed = WaveModel.wave_speed(depth)

        return distance / np.maximum(
            speed,
            1e-6
        )

    @staticmethod
    def attenuation(
        wave_height: np.ndarray,
        distance: np.ndarray
    ) -> np.ndarray:

        return wave_height / (
            1.0 + distance / 1000.0
        )

    @staticmethod
    def shoaling_factor(
        depth: np.ndarray
    ) -> np.ndarray:

        depth = np.asarray(
            depth,
            dtype=float
        )

        safe_depth = np.maximum(
            depth,
            MIN_DEPTH
        )

        factor = (
            MIN_DEPTH /
            safe_depth
        ) ** 0.25

        return np.clip(
            factor,
            0.5,
            3.0
        )