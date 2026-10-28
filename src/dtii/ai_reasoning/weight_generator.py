"""
weight_generator.py

Generates adaptive DTII weights.
"""

from __future__ import annotations


class WeightGenerator:

    def generate(self, context):

        weights = {

            "seismic": 0.20,

            "deformation": 0.20,

            "elevation": 0.15,

            "wave": 0.20,

            "inundation": 0.15,

            "prediction": 0.10,

        }

        # -------------------------

        if context.magnitude >= 8.0:

            weights["seismic"] += 0.10

            weights["elevation"] -= 0.05

            weights["prediction"] -= 0.05

        # -------------------------

        if context.wave_height >= 5:

            weights["wave"] += 0.08

            weights["prediction"] -= 0.04

            weights["inundation"] -= 0.04

        # -------------------------

        if context.prediction_error > 0.30:

            weights["prediction"] += 0.10

            weights["wave"] -= 0.05

            weights["seismic"] -= 0.05

        # -------------------------

        total = sum(weights.values())

        for key in weights:

            weights[key] /= total

        return weights