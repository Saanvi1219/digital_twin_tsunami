"""
routing.py
"""

from __future__ import annotations

import numpy as np


class FloodRouting:

    @staticmethod
    def downhill(
        elevation: np.ndarray,
    ):

        gx, gy = np.gradient(

            elevation

        )

        return (

            gx,

            gy,

        )

    # ---------------------------------------

    @staticmethod
    def flow_direction(
        elevation,
    ):

        gx, gy = np.gradient(

            elevation

        )

        return np.arctan2(

            gy,

            gx,

        )