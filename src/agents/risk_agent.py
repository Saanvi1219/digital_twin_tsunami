"""
risk_agent.py

Risk Agent
----------

Converts Digital Twin outputs into an adaptive
tsunami risk assessment.

Inputs:
- DTII
- Simulation
- Validation
- Observation

Outputs:
- Risk score
- Risk level
- Confidence
- Priority
"""

from __future__ import annotations

from typing import Any, Dict

import numpy as np


class RiskAgent:

    def __init__(self):

        self.last_result = None

    # =====================================================
    # NORMALIZATION
    # =====================================================

    @staticmethod
    def normalize(
        value: float,
        minimum: float,
        maximum: float
    ) -> float:

        if maximum <= minimum:

            return 0.0

        score = (

            (value - minimum)
            /
            (maximum - minimum)

        )

        return float(
            np.clip(
                score,
                0.0,
                1.0
            )
        )

    # =====================================================
    # RISK LEVEL
    # =====================================================

    @staticmethod
    def classify(score: float) -> str:

        if score >= 0.75:

            return "CRITICAL"

        if score >= 0.55:

            return "HIGH"

        if score >= 0.35:

            return "MODERATE"

        return "LOW"

    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(
        self,
        dtii_result: Dict[str, Any],
        simulation_result,
        validation_result: Dict[str, Any],
        observation_result: Dict[str, Any],
    ) -> Dict[str, Any]:

        print(
            "\n[RISK AGENT] "
            "Assessing tsunami risk..."
        )

        # -------------------------------------------------
        # DTII
        # -------------------------------------------------

        dtii_score = float(

            dtii_result.get(
                "score",
                0.0
            )

        )

        dtii_score = float(
            np.clip(
                dtii_score,
                0.0,
                1.0
            )
        )

        # -------------------------------------------------
        # Simulation severity
        # -------------------------------------------------

        try:

            max_wave = float(

                simulation_result.wave.max_height

            )

        except Exception:

            max_wave = 0.0

        try:

            flooded_area = float(

                simulation_result.inundation.flooded_area_km2

            )

        except Exception:

            flooded_area = 0.0

        try:

            max_depth = float(

                simulation_result.inundation.maximum_depth

            )

        except Exception:

            max_depth = 0.0

        # -------------------------------------------------
        # Normalize simulation variables
        #
        # These ranges can later be calibrated using
        # historical tsunami datasets.
        # -------------------------------------------------

        wave_score = self.normalize(

            max_wave,

            0.0,

            10.0

        )

        inundation_score = self.normalize(

            flooded_area,

            0.0,

            100.0

        )

        depth_score = self.normalize(

            max_depth,

            0.0,

            10.0

        )

        # -------------------------------------------------
        # Validation confidence
        # -------------------------------------------------

        validation_confidence = float(

            validation_result.get(
                "confidence",
                1.0
            )

        )

        validation_confidence = float(

            np.clip(
                validation_confidence,
                0.0,
                1.0
            )

        )

        # -------------------------------------------------
        # Observation anomaly
        # -------------------------------------------------

        anomaly = bool(

            observation_result.get(
                "anomaly",
                False
            )

        )

        anomaly_score = (
            1.0
            if anomaly
            else 0.0
        )

        # -------------------------------------------------
        # Risk score
        # -------------------------------------------------

        risk_score = (

            0.40 * dtii_score

            +

            0.20 * wave_score

            +

            0.15 * inundation_score

            +

            0.10 * depth_score

            +

            0.10 * anomaly_score

            +

            0.05 * validation_confidence

        )

        risk_score = float(

            np.clip(
                risk_score,
                0.0,
                1.0
            )

        )

        # -------------------------------------------------
        # Risk level
        # -------------------------------------------------

        risk_level = self.classify(
            risk_score
        )

        # -------------------------------------------------
        # Confidence
        #
        # High validation confidence increases
        # confidence in the risk assessment.
        # -------------------------------------------------

        confidence = (

            0.70 * validation_confidence

            +

            0.30 * (
                1.0 -
                float(
                    observation_result.get(
                        "change_score",
                        0.0
                    )
                )
            )

        )

        confidence = float(

            np.clip(
                confidence,
                0.0,
                1.0
            )

        )

        # -------------------------------------------------
        # Priority
        # -------------------------------------------------

        if risk_level == "CRITICAL":

            priority = "IMMEDIATE"

        elif risk_level == "HIGH":

            priority = "URGENT"

        elif risk_level == "MODERATE":

            priority = "MONITOR"

        else:

            priority = "NORMAL"

        result = {

            "risk_score":
                risk_score,

            "risk_level":
                risk_level,

            "confidence":
                confidence,

            "priority":
                priority,

            "components": {

                "dtii":
                    dtii_score,

                "wave":
                    wave_score,

                "inundation":
                    inundation_score,

                "depth":
                    depth_score,

                "observation_anomaly":
                    anomaly_score,

                "validation":
                    validation_confidence,

            },

            "simulation": {

                "max_wave":
                    max_wave,

                "flooded_area_km2":
                    flooded_area,

                "maximum_depth":
                    max_depth,

            }

        }

        self.last_result = result

        print(
            f"[RISK AGENT] "
            f"Risk Score: {risk_score:.4f}"
        )

        print(
            f"[RISK AGENT] "
            f"Risk Level: {risk_level}"
        )

        print(
            f"[RISK AGENT] "
            f"Priority: {priority}"
        )

        return result

    # =====================================================

    def last(self):

        return self.last_result