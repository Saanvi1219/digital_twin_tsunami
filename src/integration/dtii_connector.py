"""
dtii_connector.py

Connects preprocessing + simulation
to the DTII Engine.
"""

from src.dtii.dtii_engine import DTIIEngine

from .data_adapter import TsunamiFeatures


class DTIIConnector:

    def __init__(self):

        self.engine = DTIIEngine()

    # ==========================================================
    # BUILD FEATURES
    # ==========================================================

    def build_features(
        self,
        features: TsunamiFeatures,
        simulation_result: dict,
        prediction_confidence: float = 1.0,
    ):

        summary = simulation_result.get(
            "summary",
            {}
        )

        # ------------------------------------------------------
        # Earthquake magnitude
        # ------------------------------------------------------

        seismic = float(
            features.earthquake.magnitude
        )

        # ------------------------------------------------------
        # Ground deformation
        # ------------------------------------------------------

        deformation = float(
            getattr(
                features,
                "ground_deformation",
                0.0
            )
        )

        # ------------------------------------------------------
        # Mean elevation
        # ------------------------------------------------------

        elevation = float(
            getattr(
                features,
                "mean_elevation",
                0.0
            )
        )

        # ------------------------------------------------------
        # Wave height
        # ------------------------------------------------------

        wave = float(
            summary.get(
                "max_wave",
                0.0
            )
        )

        # ------------------------------------------------------
        # Flooded area
        # ------------------------------------------------------

        inundation = float(
            summary.get(
                "flooded_area",
                0.0
            )
        )

        # ------------------------------------------------------
        # Prediction confidence
        # ------------------------------------------------------

        prediction = float(
            prediction_confidence
        )

        return {

            "seismic":
                seismic,

            "deformation":
                deformation,

            "elevation":
                elevation,

            "wave":
                wave,

            "inundation":
                inundation,

            "prediction":
                prediction,

        }

    # ==========================================================
    # COMPUTE
    # ==========================================================

    def compute(
        self,
        features: TsunamiFeatures,
        simulation_result: dict,
        prediction_confidence: float = 1.0,
    ):

        dtii_features = self.build_features(

            features,

            simulation_result,

            prediction_confidence,

        )

        result = self.engine.compute(
            dtii_features
        )

        # Keep raw features for debugging
        result["raw_features"] = (
            dtii_features
        )

        return result

    # ==========================================================
    # SUMMARY
    # ==========================================================

    def summary(
        self,
        result
    ):

        return self.engine.summary(
            result
        )