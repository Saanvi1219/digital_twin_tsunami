"""
observation_agent.py

Observation Agent
-----------------

Responsible for:

- Monitoring incoming tsunami observations
- Comparing current observations with previous state
- Detecting significant changes
- Producing observation confidence
- Triggering adaptive re-simulation when necessary
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import numpy as np


@dataclass
class ObservationResult:

    changed: bool

    anomaly: bool

    change_score: float

    observation_confidence: float

    changes: Dict[str, float]

    message: str


class ObservationAgent:

    """
    Monitors environmental observations and determines
    whether the Digital Twin needs to adapt.
    """

    def __init__(
        self,
        change_threshold: float = 0.10,
        anomaly_threshold: float = 0.30,
    ):

        self.change_threshold = change_threshold
        self.anomaly_threshold = anomaly_threshold

        self.previous_observation: Optional[Dict[str, float]] = None

        self.last_result: Optional[ObservationResult] = None

    # =====================================================
    # SAFE NUMERIC CONVERSION
    # =====================================================

    @staticmethod
    def _safe_float(value: Any) -> float:

        try:

            value = float(value)

            if np.isnan(value) or np.isinf(value):
                return 0.0

            return value

        except Exception:

            return 0.0

    # =====================================================
    # EXTRACT OBSERVATION FEATURES
    # =====================================================

    def extract_observation(self, features) -> Dict[str, float]:

        earthquake = getattr(
            features,
            "earthquake",
            None
        )

        return {

            "magnitude":
                self._safe_float(
                    getattr(
                        earthquake,
                        "magnitude",
                        0.0
                    )
                ),

            "ground_deformation":
                self._safe_float(
                    getattr(
                        features,
                        "ground_deformation",
                        0.0
                    )
                ),

            "mean_elevation":
                self._safe_float(
                    getattr(
                        features,
                        "mean_elevation",
                        0.0
                    )
                ),

            "mean_bathymetry":
                self._safe_float(
                    getattr(
                        features,
                        "mean_bathymetry",
                        0.0
                    )
                ),

            "mean_ndwi":
                self._safe_float(
                    getattr(
                        features,
                        "mean_ndwi",
                        0.0
                    )
                ),

            "inundation_area":
                self._safe_float(
                    getattr(
                        features,
                        "inundation_area",
                        0.0
                    )
                ),
        }

    # =====================================================
    # NORMALIZED CHANGE
    # =====================================================

    @staticmethod
    def _relative_change(
        current: float,
        previous: float
    ) -> float:

        denominator = max(
            abs(previous),
            1e-8
        )

        return abs(
            current - previous
        ) / denominator

    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(self, features) -> Dict[str, Any]:

        print("\n[OBSERVATION AGENT] Monitoring observations...")

        current = self.extract_observation(
            features
        )

        # -------------------------------------------------
        # First observation
        # -------------------------------------------------

        if self.previous_observation is None:

            self.previous_observation = current

            result = ObservationResult(

                changed=False,

                anomaly=False,

                change_score=0.0,

                observation_confidence=1.0,

                changes={},

                message="Initial observation registered."

            )

            self.last_result = result

            print(
                "[OBSERVATION AGENT] Initial observation stored."
            )

            return self._to_dict(result)

        # -------------------------------------------------
        # Compare observations
        # -------------------------------------------------

        changes = {}

        for key, current_value in current.items():

            previous_value = self.previous_observation.get(
                key,
                0.0
            )

            changes[key] = self._relative_change(
                current_value,
                previous_value
            )

        # -------------------------------------------------
        # Overall change score
        # -------------------------------------------------

        if changes:

            change_score = float(
                np.mean(
                    list(changes.values())
                )
            )

        else:

            change_score = 0.0

        # -------------------------------------------------
        # Significant changes
        # -------------------------------------------------

        significant_changes = {

            key: value

            for key, value in changes.items()

            if value >= self.change_threshold

        }

        changed = (
            len(significant_changes) > 0
        )

        # -------------------------------------------------
        # Anomaly
        # -------------------------------------------------

        anomaly = (

            any(
                value >= self.anomaly_threshold
                for value in changes.values()
            )

        )

        # -------------------------------------------------
        # Confidence
        # -------------------------------------------------

        confidence = max(

            0.0,

            min(

                1.0,

                1.0 - change_score

            )

        )

        if anomaly:

            message = (
                "Significant observation anomaly detected."
            )

        elif changed:

            message = (
                "Environmental state changed; "
                "adaptive update recommended."
            )

        else:

            message = (
                "Observations remain stable."
            )

        # -------------------------------------------------
        # Store current state
        # -------------------------------------------------

        self.previous_observation = current

        result = ObservationResult(

            changed=changed,

            anomaly=anomaly,

            change_score=change_score,

            observation_confidence=confidence,

            changes=significant_changes,

            message=message

        )

        self.last_result = result

        print(
            "[OBSERVATION AGENT]",
            message
        )

        print(
            "[OBSERVATION AGENT] "
            f"Change score: {change_score:.4f}"
        )

        return self._to_dict(result)

    # =====================================================
    # SERIALIZATION
    # =====================================================

    @staticmethod
    def _to_dict(
        result: ObservationResult
    ) -> Dict[str, Any]:

        return {

            "changed":
                result.changed,

            "anomaly":
                result.anomaly,

            "change_score":
                result.change_score,

            "observation_confidence":
                result.observation_confidence,

            "changes":
                result.changes,

            "message":
                result.message,

        }

    # =====================================================

    def reset(self):

        self.previous_observation = None

        self.last_result = None