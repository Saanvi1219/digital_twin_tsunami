"""
state_mapper.py

Maps Digital Twin state into DTII features.
"""

from __future__ import annotations


class StateMapper:
    """
    Converts Digital Twin state into
    DTII features.
    """

    REQUIRED_FEATURES = [

        "seismic",

        "deformation",

        "elevation",

        "wave",

        "inundation",

        "prediction",

    ]

    # ==========================================================
    # FROM DICTIONARY
    # ==========================================================

    @staticmethod
    def from_dict(
        features: dict
    ):

        for key in StateMapper.REQUIRED_FEATURES:

            if key not in features:

                raise KeyError(
                    f"Missing feature: {key}"
                )

        return {

            "seismic":
                float(
                    features["seismic"]
                ),

            "deformation":
                float(
                    features["deformation"]
                ),

            "elevation":
                float(
                    features["elevation"]
                ),

            "wave":
                float(
                    features["wave"]
                ),

            "inundation":
                float(
                    features["inundation"]
                ),

            "prediction":
                float(
                    features["prediction"]
                ),

        }

    # ==========================================================
    # PLACEHOLDER
    # ==========================================================

    @staticmethod
    def placeholder():

        return {

            "seismic":
                7.5,

            "deformation":
                0.35,

            "elevation":
                20.0,

            "wave":
                2.5,

            "inundation":
                50.0,

            "prediction":
                0.90,

        }