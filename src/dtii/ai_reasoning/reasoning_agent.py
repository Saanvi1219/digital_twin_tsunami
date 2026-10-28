"""
reasoning_agent.py

Gemini-powered adaptive DTII reasoning agent.

Responsibilities:
- Analyze tsunami context
- Generate adaptive DTII weights
- Provide reasoning explanation
- Provide confidence score
- Validate AI output
"""

from __future__ import annotations

import json
import os

import google.generativeai as genai

from .context import TsunamiContext
from .prompt_builder import PromptBuilder
from .weight_validator import WeightValidator


class GeminiReasoningAgent:
    """
    Adaptive DTII reasoning agent powered by Gemini.
    """

    def __init__(self):

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:

            raise ValueError(
                "GEMINI_API_KEY not found."
            )

        genai.configure(
            api_key=api_key
        )

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )


    # -------------------------------------------------

    def _clean_response(self, text: str):

        """
        Removes markdown formatting
        from Gemini JSON response.
        """

        text = text.strip()

        if text.startswith("```"):

            text = text.replace(
                "```json",
                ""
            )

            text = text.replace(
                "```",
                ""
            )

        return text.strip()


    # -------------------------------------------------

    def _fallback_response(self):

        """
        Safe fallback if Gemini fails.

        Uses balanced DTII weights.
        """

        return {

            "weights": {

                "seismic": 0.20,

                "deformation": 0.20,

                "elevation": 0.15,

                "wave": 0.20,

                "inundation": 0.15,

                "prediction": 0.10,

            },

            "reasoning":

                "Fallback weights used because AI reasoning was unavailable.",


            "confidence":

                0.0

        }


    # -------------------------------------------------

    def generate_weights(
        self,
        context: TsunamiContext,
    ):

        """
        Generate adaptive DTII weights.

        Returns:
        {
            weights,
            reasoning,
            confidence
        }
        """

        try:

            # Build Gemini prompt

            prompt = PromptBuilder.build(
                context
            )


            response = self.model.generate_content(
                prompt
            )


            text = self._clean_response(
                response.text
            )


            result = json.loads(
                text
            )


            # Validate AI weights

            weights = WeightValidator.validate_and_normalize(
                result["weights"]
            )


            confidence = result.get(
                "confidence",
                0.8
            )


            reasoning = result.get(
                "reasoning",
                "No reasoning provided."
            )


            return {

                "weights": weights,

                "reasoning": reasoning,

                "confidence": confidence

            }


        except Exception as e:


            print(
                f"[WARNING] Gemini reasoning failed: {e}"
            )


            return self._fallback_response()