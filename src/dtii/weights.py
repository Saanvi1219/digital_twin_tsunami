"""
weights.py

Static DTII weights.

Later these will be replaced
by the AI Reasoning Agent.
"""

DEFAULT_WEIGHTS = {

    "seismic": 0.20,

    "deformation": 0.20,

    "elevation": 0.15,

    "wave": 0.20,

    "inundation": 0.15,

    "prediction": 0.10,

}


def validate_weights(weights):

    total = sum(weights.values())

    if abs(total - 1.0) > 1e-6:

        raise ValueError(

            f"Weights must sum to 1. Current={total}"

        )

    return True