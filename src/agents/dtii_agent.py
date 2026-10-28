"""
dtii_agent.py

Responsible for:
- Computing DTII score
- Estimating tsunami hazard level
"""

from src.integration.dtii_connector import DTIIConnector


class DTIIAgent:

    def __init__(self):

        self.connector = DTIIConnector()

    # =====================================================

    def execute(

        self,

        features,

        simulation_summary,

        prediction_confidence=1.0,

    ):

        print("\n[DTII AGENT] Computing DTII...")

        dtii_result = self.connector.compute(

            features,

            simulation_summary,

            prediction_confidence,

        )

        print("[DTII AGENT] DTII computation completed.")

        return dtii_result

    # =====================================================

    def summary(

        self,

        dtii_result,

    ):

        return self.connector.summary(

            dtii_result

        )