"""
dtii_engine.py

Main DTII Engine.

Coordinates:

- State Mapping
- Feature Normalization
- DTII Score Computation
- Risk Classification
"""

from __future__ import annotations

from .state_mapper import StateMapper
from .normalizer import Normalizer
from .scorer import DTIIScorer


class DTIIEngine:
    """
    Digital Twin Tsunami Intelligence Index Engine.
    """

    def __init__(self, weights=None):

        self.mapper = StateMapper()

        self.normalizer = Normalizer()

        self.scorer = DTIIScorer(
            weights
        )

    # ==========================================================
    # FEATURE NORMALIZATION
    # ==========================================================

    def preprocess_features(
        self,
        features: dict
    ) -> dict:

        normalized = {}

        for key, value in features.items():

            normalized[key] = (
                self.normalizer.normalize_feature(
                    value,
                    key
                )
            )

        return normalized

    # ==========================================================
    # COMPUTE
    # ==========================================================

    def compute(
        self,
        features: dict
    ) -> dict:

        # ---------------------------------------------
        # Validate required features
        # ---------------------------------------------

        mapped = self.mapper.from_dict(
            features
        )

        # ---------------------------------------------
        # Normalize feature-by-feature
        # ---------------------------------------------

        normalized = self.preprocess_features(
            mapped
        )

        # ---------------------------------------------
        # Calculate weighted DTII
        # ---------------------------------------------

        score = self.scorer.score(
            normalized
        )

        # ---------------------------------------------
        # Classification
        # ---------------------------------------------

        level = self.scorer.classify(
            score
        )

        return {

            "score":
                score,

            "level":
                level,

            "features":
                normalized,

        }

    # ==========================================================
    # PLACEHOLDER
    # ==========================================================

    def compute_placeholder(self):

        features = self.mapper.placeholder()

        return self.compute(
            features
        )

    # ==========================================================
    # SUMMARY
    # ==========================================================

    def summary(
        self,
        result
    ):

        print(
            "\n" + "=" * 50
        )

        print(
            " DIGITAL TWIN INTELLIGENCE INDEX "
        )

        print(
            "=" * 50
        )

        print(
            f"Score : {result['score']:.4f}"
        )

        print(
            f"Level : {result['level']}"
        )

        print(
            "\nFeatures"
        )

        for key, value in result[
            "features"
        ].items():

            print(
                f"  {key:15} : {value:.3f}"
            )

        print(
            "=" * 50
        )