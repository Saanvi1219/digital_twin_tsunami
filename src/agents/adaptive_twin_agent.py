"""
adaptive_twin_agent.py

Adaptive Digital Twin Agent.

Responsibilities
----------------
- Maintain Digital Twin state
- Detect observation changes
- Decide whether adaptation is required
- Update Digital Twin state
- Track confidence
- Track DTII before/after adaptation
"""

from __future__ import annotations

from typing import Any, Dict

from src.agents.twin_agent import TwinAgent


class AdaptiveTwinAgent:

    def __init__(
        self,
        adaptation_threshold: float = 0.10
    ):

        self.twin_agent = TwinAgent()

        self.adaptation_threshold = (
            adaptation_threshold
        )

        self.last_observation = None

        self.last_confidence = 1.0

        self.adaptation_count = 0

        self.previous_dtii = None

        self.current_dtii = None

    # ==========================================================
    # INITIALIZE
    # ==========================================================

    def initialize(
        self,
        features,
        simulation_result,
        dtii_result
    ):

        print(
            "\n[ADAPTIVE TWIN AGENT] "
            "Initializing adaptive Digital Twin..."
        )

        self.current_dtii = dtii_result

        if isinstance(
            dtii_result,
            dict
        ):

            self.previous_dtii = (
                dtii_result.get(
                    "score"
                )
            )

        twin = self.twin_agent.execute(

            features,

            simulation_result,

            dtii_result,

        )

        self.last_confidence = 1.0

        print(
            "[ADAPTIVE TWIN AGENT] "
            "Digital Twin initialized."
        )

        return twin

    # ==========================================================
    # OBSERVATION
    # ==========================================================

    def update_from_observation(
        self,
        observation: Dict[str, Any]
    ) -> Dict[str, Any]:

        self.last_observation = (
            observation
        )

        change_score = float(
            observation.get(
                "change_score",
                0.0
            )
        )

        changed = bool(
            observation.get(
                "changed",
                False
            )
        )

        anomaly = bool(
            observation.get(
                "anomaly",
                False
            )
        )

        confidence = float(
            observation.get(
                "observation_confidence",
                1.0
            )
        )

        adaptation_required = (

            changed

            or

            anomaly

            or

            change_score
            >=
            self.adaptation_threshold

        )

        if adaptation_required:

            self.adaptation_count += 1

        self.last_confidence = confidence

        result = {

            "adaptation_required":
                adaptation_required,

            "change_score":
                change_score,

            "observation_confidence":
                confidence,

            "adaptation_count":
                self.adaptation_count,

            "reason":

                (
                    "Observation change detected."
                    if adaptation_required
                    else
                    "No adaptation required."
                )

        }

        print(
            "\n[ADAPTIVE TWIN AGENT]"
        )

        print(
            "Adaptation required:",
            adaptation_required
        )

        print(
            "Observation confidence:",
            round(
                confidence,
                4
            )
        )

        return result

    # ==========================================================
    # UPDATE DIGITAL TWIN
    # ==========================================================

    def update(
        self,
        simulation_result,
        dtii_result,
        validation_result=None,
        features=None
    ):

        print(
            "\n[ADAPTIVE TWIN AGENT] "
            "Updating Digital Twin..."
        )

        # ------------------------------------------------------
        # Validation
        # ------------------------------------------------------

        if validation_result is not None:

            dtii_result = dict(
                dtii_result
            )

            dtii_result[
                "validation"
            ] = validation_result

            if "confidence" in validation_result:

                self.last_confidence = float(
                    validation_result[
                        "confidence"
                    ]
                )

        # ------------------------------------------------------
        # DTII tracking
        # ------------------------------------------------------

        if self.current_dtii is not None:

            if isinstance(
                self.current_dtii,
                dict
            ):

                self.previous_dtii = (
                    self.current_dtii.get(
                        "score"
                    )
                )

        self.current_dtii = dtii_result

        # ------------------------------------------------------
        # Store actual preprocessing state
        # ------------------------------------------------------

        twin = (
            self.twin_agent.connector.twin
        )

        if features is not None:

            twin.update(

                earthquake=
                    features.earthquake,

                dem=
                    features.dem,

                bathymetry=
                    features.bathymetry,

                sentinel1=
                    features.sentinel1,

                sentinel2=
                    features.sentinel2,

                altimetry=
                    features.altimetry,

                simulation_result=
                    simulation_result,

                tsunami=
                    simulation_result,

                prediction=
                    dtii_result,

                confidence=
                    self.last_confidence,

            )

        else:

            self.twin_agent.connector.update_results(

                simulation_result,

                dtii_result,

            )

        # ------------------------------------------------------
        # Metadata
        # ------------------------------------------------------

        twin.update_metadata(

            adaptive=True,

            adaptation_count=
                self.adaptation_count,

            prediction_confidence=
                self.last_confidence,

        )

        print(
            "[ADAPTIVE TWIN AGENT] "
            "Twin state adapted successfully."
        )

        return self.twin_agent.get()

    # ==========================================================
    # HEALTH
    # ==========================================================

    def health(self):

        return self.twin_agent.health()

    # ==========================================================
    # SUMMARY
    # ==========================================================

    def summary(self):

        return {

            "twin":
                self.twin_agent.summary(),

            "adaptation_count":
                self.adaptation_count,

            "last_confidence":
                self.last_confidence,

            "previous_dtii":
                self.previous_dtii,

            "current_dtii":
                (
                    self.current_dtii.get(
                        "score"
                    )
                    if isinstance(
                        self.current_dtii,
                        dict
                    )
                    else None
                ),

        }

    # ==========================================================
    # GET
    # ==========================================================

    def get(self):

        return self.twin_agent.get()