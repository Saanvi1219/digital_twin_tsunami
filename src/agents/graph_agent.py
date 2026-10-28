"""
graph_agent.py

Responsible for:
- Building the Graph Digital Twin
- Updating graph nodes
"""

from src.digital_twin.graph_builder import GraphBuilder


class GraphAgent:

    def __init__(self):

        self.builder = GraphBuilder()

    # =====================================================

    def execute(

        self,

        features,

        simulation_summary,

        dtii_result,

    ):

        print("\n[GRAPH AGENT] Building Graph Digital Twin...")

        graph = self.builder.build(

            magnitude=features.earthquake.magnitude,

            deformation=features.ground_deformation,

            elevation=features.mean_elevation,

            bathymetry=features.mean_bathymetry,

            wave_height=simulation_summary["max_wave"],

            inundation=simulation_summary["flooded_area"],

            prediction=1.0,

            dtii_score=dtii_result["score"],

            risk_level=dtii_result["level"],

        )

        print("[GRAPH AGENT] Graph created successfully.")

        return graph

    # =====================================================

    def update(

        self,

        node,

        value,

    ):

        self.builder.update(

            node,

            value,

        )

    # =====================================================

    def get_graph(self):

        return self.builder.get_graph()