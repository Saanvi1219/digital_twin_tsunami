"""
weight_validator.py

Validates and normalizes Gemini-generated DTII weights.
"""

from __future__ import annotations


REQUIRED_KEYS = [

    "seismic",

    "deformation",

    "elevation",

    "wave",

    "inundation",

    "prediction",

]


class WeightValidator:

    """
    Validates AI-generated DTII weights.
    """

    # --------------------------------------------------

    @staticmethod
    def validate(weights: dict):

        # -------------------------------
        # Check keys
        # -------------------------------

        for key in REQUIRED_KEYS:

            if key not in weights:

                raise KeyError(

                    f"Missing weight: {key}"

                )

        # -------------------------------
        # Check values
        # -------------------------------

        for key, value in weights.items():

            if not isinstance(

                value,

                (int, float),

            ):

                raise TypeError(

                    f"{key} must be numeric."

                )

            if value < 0:

                raise ValueError(

                    f"{key} cannot be negative."

                )

        return True

    # --------------------------------------------------

    @staticmethod
    def normalize(weights: dict):

        total = sum(weights.values())

        if total == 0:

            raise ValueError(

                "Weight sum cannot be zero."

            )

        normalized = {}

        for key, value in weights.items():

            normalized[key] = value / total

        return normalized

    # --------------------------------------------------

    @staticmethod
    def validate_and_normalize(weights):

        WeightValidator.validate(weights)

        return WeightValidator.normalize(weights)