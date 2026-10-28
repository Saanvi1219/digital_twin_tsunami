"""
scorer.py

Computes DTII score.
"""

from __future__ import annotations

from .weights import DEFAULT_WEIGHTS
from .weights import validate_weights


class DTIIScorer:

    """
    DTII Scoring Engine.
    """

    def __init__(

        self,

        weights=None,

    ):

        if weights is None:

            weights = DEFAULT_WEIGHTS

        validate_weights(weights)

        self.weights = weights

    # -------------------------------------------------

    def score(

        self,

        features,

    ):

        score = 0.0

        for feature, value in features.items():

            score += (

                value *

                self.weights[feature]

            )

        return round(score, 4)

    # -------------------------------------------------

    @staticmethod
    def classify(score):

        if score < 0.20:

            return "Very Low"

        elif score < 0.40:

            return "Low"

        elif score < 0.60:

            return "Moderate"

        elif score < 0.80:

            return "High"

        else:

            return "Very High"