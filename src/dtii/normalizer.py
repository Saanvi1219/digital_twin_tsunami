"""
normalizer.py

DTII feature normalization.

Converts tsunami-related physical features
into comparable [0,1] scores.

Higher score = greater tsunami significance/risk,
except elevation where lower elevation means
greater tsunami susceptibility.
"""

from __future__ import annotations

import numpy as np


class Normalizer:

    # ==========================================================
    # GENERIC MIN-MAX
    # ==========================================================

    @staticmethod
    def minmax(
        value,
        minimum,
        maximum,
    ):

        if maximum <= minimum:
            return 0.0

        score = (
            float(value) - minimum
        ) / (
            maximum - minimum
        )

        return float(
            np.clip(
                score,
                0.0,
                1.0
            )
        )

    # ==========================================================
    # CLIP
    # ==========================================================

    @staticmethod
    def clip(value):

        return float(
            np.clip(
                float(value),
                0.0,
                1.0
            )
        )

    # ==========================================================
    # FEATURE-SPECIFIC NORMALIZATION
    # ==========================================================

    @staticmethod
    def normalize_feature(
        feature,
        key=None
    ):

        value = float(feature)

        # ------------------------------------------------------
        # SEISMIC MAGNITUDE
        # Typical tsunami-relevant range: M4 - M9
        # ------------------------------------------------------

        if key == "seismic":

            return Normalizer.minmax(
                value,
                4.0,
                9.0
            )

        # ------------------------------------------------------
        # GROUND DEFORMATION
        # Assumed normalized deformation if already [0,1].
        #
        # If your preprocessing later provides deformation
        # in metres, this range can be calibrated.
        # ------------------------------------------------------

        if key == "deformation":

            return Normalizer.minmax(
                value,
                0.0,
                1.0
            )

        # ------------------------------------------------------
        # ELEVATION
        #
        # LOW elevation = HIGH tsunami susceptibility.
        #
        # 0 m -> 1
        # 100 m+ -> 0
        # ------------------------------------------------------

        if key == "elevation":

            elevation_score = 1.0 - Normalizer.minmax(
                value,
                0.0,
                100.0
            )

            return Normalizer.clip(
                elevation_score
            )

        # ------------------------------------------------------
        # WAVE HEIGHT
        #
        # 0 m -> 0
        # 10 m+ -> 1
        # ------------------------------------------------------

        if key == "wave":

            return Normalizer.minmax(
                value,
                0.0,
                10.0
            )

        # ------------------------------------------------------
        # INUNDATION AREA
        #
        # 0 km² -> 0
        # 100 km²+ -> 1
        # ------------------------------------------------------

        if key == "inundation":

            return Normalizer.minmax(
                value,
                0.0,
                100.0
            )

        # ------------------------------------------------------
        # MODEL PREDICTION CONFIDENCE
        #
        # Already expected to be [0,1].
        # ------------------------------------------------------

        if key == "prediction":

            return Normalizer.clip(
                value
            )

        # ------------------------------------------------------
        # FALLBACK
        # ------------------------------------------------------

        return Normalizer.clip(
            value
        )