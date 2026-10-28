"""
demo_inputs.py

Temporary synthetic inputs used ONLY for
integration testing when real DEM/bathymetry
data are unavailable.

These must NOT be used for scientific results.
"""

from pathlib import Path

import numpy as np


def create_demo_dem(shape=(256, 256)):

    rows, cols = shape

    y, x = np.indices(shape)

    # Smooth synthetic coastal terrain
    dem = (
        2.0
        + 0.02 * x
        + 0.015 * y
    )

    return dem.astype(float)


def create_demo_bathymetry(shape=(256, 256)):

    rows, cols = shape

    y, x = np.indices(shape)

    # Positive water-depth representation
    bathymetry = (
        50.0
        + 0.10 * x
        + 0.08 * y
    )

    return bathymetry.astype(float)


def create_demo_inputs(shape=(256, 256)):

    return {

        "dem": create_demo_dem(shape),

        "bathymetry":
            create_demo_bathymetry(shape),

    }