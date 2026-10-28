"""
utils.py

Common utilities for tsunami simulation.
"""

from __future__ import annotations

import numpy as np


# =====================================================
# Grid Utilities
# =====================================================


def validate_grid(
    grid: np.ndarray,
    name: str = "Grid"
):
    """
    Validate raster grid.
    """

    if not isinstance(grid, np.ndarray):

        raise TypeError(

            f"{name} must be numpy.ndarray"

        )

    if grid.ndim != 2:

        raise ValueError(

            f"{name} must be 2D"

        )

    return True



# =====================================================
# Normalization
# =====================================================


def normalize(
    data: np.ndarray
):

    """
    Min-max normalization.
    """

    minimum = np.min(data)

    maximum = np.max(data)

    return (

        data - minimum

    ) / (

        maximum - minimum + 1e-9

    )



# =====================================================
# Statistics
# =====================================================


def raster_statistics(
    data: np.ndarray
):

    """
    Generate raster statistics.
    """

    return {

        "min":

            float(np.min(data)),

        "max":

            float(np.max(data)),

        "mean":

            float(np.mean(data)),

        "std":

            float(np.std(data)),

        "shape":

            data.shape,

    }



# =====================================================
# Distance
# =====================================================


def euclidean_distance(
    point1,
    point2
):

    """
    Calculate distance between two points.
    """

    return np.sqrt(

        (point1[0]-point2[0])**2 +

        (point1[1]-point2[1])**2

    )



# =====================================================
# Threshold
# =====================================================


def apply_threshold(
    data: np.ndarray,

    threshold: float
):

    """
    Create binary mask.
    """

    return data > threshold