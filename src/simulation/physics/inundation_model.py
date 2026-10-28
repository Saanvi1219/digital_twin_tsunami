"""
inundation_model.py

Tsunami inundation calculations.
"""

from __future__ import annotations

import numpy as np


class InundationModel:

    @staticmethod
    def flood_depth(
        wave: np.ndarray,
        elevation: np.ndarray,
        coastal_reference: float = 0.0
    ) -> np.ndarray:

        wave = np.asarray(
            wave,
            dtype=float
        )

        elevation = np.asarray(
            elevation,
            dtype=float
        )

        relative_elevation = (
            elevation - coastal_reference
        )

        flood_depth = (
            wave - relative_elevation
        )

        return np.maximum(
            flood_depth,
            0.0
        )

    @staticmethod
    def inundation_mask(
        flood_depth: np.ndarray,
        threshold: float = 0.05
    ) -> np.ndarray:

        return (
            np.asarray(flood_depth) >
            threshold
        )

    @staticmethod
    def limit_to_land(
        flood_depth: np.ndarray,
        elevation: np.ndarray,
        sea_level: float = 0.0
    ) -> np.ndarray:

        land_mask = (
            np.asarray(elevation) >= sea_level
        )

        return np.where(
            land_mask,
            flood_depth,
            0.0
        )