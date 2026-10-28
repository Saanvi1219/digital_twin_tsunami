"""
twin_agent.py

Responsible for:
- Initializing the Digital Twin
- Updating the Twin using Simulation + DTII
- Monitoring Twin health
"""

from src.integration.twin_connector import TwinConnector


class TwinAgent:

    def __init__(self):

        self.connector = TwinConnector()

    # =====================================================

    def execute(

        self,

        features,

        simulation_result,

        dtii_result,

    ):

        print("\n[TWIN AGENT] Initializing Digital Twin...")

        twin = self.connector.initialize(

            features

        )

        print("[TWIN AGENT] Updating Twin State...")

        self.connector.update_results(

            simulation_result,

            dtii_result,

        )

        print("[TWIN AGENT] Twin updated successfully.")

        return twin

    # =====================================================

    def validate(self):

        return self.connector.validate()

    # =====================================================

    def summary(self):

        return self.connector.summary()

    # =====================================================

    def health(self):

        return self.connector.health()

    # =====================================================

    def get(self):

        return self.connector.get()