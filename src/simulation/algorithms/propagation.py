"""
propagation.py

Tsunami wave propagation algorithms.
"""

from __future__ import annotations

import numpy as np


class WavePropagation:

    @staticmethod
    def radial_decay(
        wave_height: np.ndarray,
        distance: np.ndarray,
        attenuation_factor: float = 1000.0
    ) -> np.ndarray:

        distance = np.asarray(
            distance,
            dtype=float
        )

        return wave_height / (
            1.0 +
            distance / attenuation_factor
        )

    @staticmethod
    def apply_travel_time(
        wave_height: np.ndarray,
        travel_time: np.ndarray,
        damping: float = 0.001,
        max_travel_time: float = 10800.0
    ) -> np.ndarray:

        # ------------------------------------------------------
        # FIX: travel_time can blow up to tens of thousands of
        # seconds wherever water_depth gets clamped to
        # MIN_DEPTH (shallow/land-adjacent/invalid bathymetry),
        # since wave_speed = sqrt(g * depth) collapses there.
        # exp(-damping * travel_time) then underflows toward 0,
        # and that near-zero propagates through the whole
        # pipeline. Clipping travel_time bounds how much damping
        # any single pixel can receive.
        # ------------------------------------------------------

        travel_time = np.asarray(
            travel_time,
            dtype=float
        )

        travel_time = np.clip(
            travel_time,
            0.0,
            max_travel_time
        )

        return (
            wave_height *
            np.exp(
                -damping *
                travel_time
            )
        )

    @staticmethod
    def clip(
        wave_height: np.ndarray,
        minimum: float = 0.0,
        maximum: float = 100.0
    ) -> np.ndarray:

        return np.clip(
            wave_height,
            minimum,
            maximum
        )

    @staticmethod
    def normalize(
        wave_height: np.ndarray
    ) -> np.ndarray:

        wave_height = np.asarray(
            wave_height,
            dtype=float
        )

        maximum = np.max(
            wave_height
        )

        if maximum <= 0:
            return np.zeros_like(
                wave_height
            )

        return (
            wave_height /
            maximum
        )

    @staticmethod
    def gaussian_source(
        shape,
        amplitude: float,
        sigma: float = 35.0,
        center=None
    ) -> np.ndarray:

        rows, cols = shape

        yy, xx = np.indices(
            shape,
            dtype=float
        )

        if center is None:
            center_y = (rows - 1) / 2.0
            center_x = (cols - 1) / 2.0
        else:
            center_y, center_x = center

        distance_squared = (
            (xx - center_x) ** 2 +
            (yy - center_y) ** 2
        )

        source = amplitude * np.exp(
            -distance_squared /
            (2.0 * sigma ** 2)
        )

        return source