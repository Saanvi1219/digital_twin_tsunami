"""
test_reasoning.py
"""

from src.dtii.ai_reasoning.context import TsunamiContext
from src.dtii.ai_reasoning.reasoning_agent import GeminiReasoningAgent


def main():

    context = TsunamiContext(

        magnitude=8.2,

        wave_height=6.1,

        bathymetry_depth=4200,

        coastal_slope=0.18,

        inundation_area=58,

        prediction_error=0.12,

        sensor_confidence=0.95,

    )

    agent = GeminiReasoningAgent()

    response = agent.generate_weights(context)

    print("\nWeights\n")

    print(response["weights"])

    print("\nReasoning\n")

    print(response["reasoning"])


if __name__ == "__main__":

    main()