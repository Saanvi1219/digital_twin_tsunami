"""
prompt_builder.py

Creates Gemini prompts for adaptive DTII.
"""

from __future__ import annotations

from .context import TsunamiContext


class PromptBuilder:

    @staticmethod
    def build(context: TsunamiContext):

        return f"""
You are an AI reasoning engine inside an Adaptive Tsunami Digital Twin.

Analyze the tsunami situation.

Assign importance weights to:

1. seismic
2. deformation
3. elevation
4. wave
5. inundation
6. prediction

Rules

- Sum must equal 1.0
- Every value must be between 0 and 1
- Return ONLY JSON.

Context

Magnitude: {context.magnitude}

Wave Height: {context.wave_height}

Bathymetry Depth: {context.bathymetry_depth}

Coastal Slope: {context.coastal_slope}

Inundation Area: {context.inundation_area}

Prediction Error: {context.prediction_error}

Sensor Confidence: {context.sensor_confidence}

Return EXACTLY this format

{{
    "weights": {{

        "seismic": 0,

        "deformation": 0,

        "elevation": 0,

        "wave": 0,

        "inundation": 0,

        "prediction": 0

    }},

    "reasoning":

    "Explain why these weights were chosen."
}}
"""