"""
llm_agent.py

Multi-agent wrapper around the Gemini tsunami
Decision Intelligence Agent.
"""

from llm.gemini_agent import GeminiTsunamiAgent


class LLMAgent:

    def __init__(self):

        self.agent = GeminiTsunamiAgent()

    # ======================================================

    def execute(
        self,
        features,
        simulation_summary,
        dtii,
        twin_state=None,
    ):

        print("\n[LLM AGENT] Starting Gemini analysis...")

        result = self.agent.analyse(

            features=features,

            simulation_summary=simulation_summary,

            dtii=dtii,

            twin_state=twin_state,

        )

        print(
            "[LLM AGENT] Gemini analysis completed."
        )

        return result
    