"""
simulation_agent.py

Responsible for:
- Running tsunami simulation
- Returning simulation outputs
"""

from src.integration.simulation_connector import SimulationConnector


class SimulationAgent:

    def __init__(self):

        self.connector = SimulationConnector()

    # =====================================================

    def execute(

        self,

        features,

    ):

        print("\n[SIMULATION AGENT] Starting tsunami simulation...")

        simulation_result = self.connector.run(

            features

        )

        simulation_summary = self.connector.summary()

        print("[SIMULATION AGENT] Simulation completed.")

        return {

            "result": simulation_result,

            "summary": simulation_summary,

        }

    # =====================================================

    def last_result(self):

        return self.connector.last_result

    # =====================================================

    def summary(self):

        return self.connector.summary()