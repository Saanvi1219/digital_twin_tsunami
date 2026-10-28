"""
graph_builder.py

Builds the Graph-Based Digital Twin automatically.
"""

from .graph_twin import GraphDigitalTwin


class GraphBuilder:

    def __init__(self):

        self.graph = GraphDigitalTwin()

    # ---------------------------------------------------------

    def build(
        self,
        magnitude,
        deformation,
        elevation,
        bathymetry,
        wave_height,
        inundation,
        prediction,
        dtii_score,
        risk_level,
    ):

        # ---------------- Nodes ----------------

        self.graph.add_node(
            "Earthquake",
            magnitude
        )

        self.graph.add_node(
            "Ground Deformation",
            deformation
        )

        self.graph.add_node(
            "Elevation",
            elevation
        )

        self.graph.add_node(
            "Bathymetry",
            bathymetry
        )

        self.graph.add_node(
            "Wave Height",
            wave_height
        )

        self.graph.add_node(
            "Inundation",
            inundation
        )

        self.graph.add_node(
            "Prediction",
            prediction
        )

        self.graph.add_node(
            "DTII",
            dtii_score
        )

        self.graph.add_node(
            "Risk",
            risk_level
        )

        # ---------------- Relationships ----------------

        self.graph.add_edge(
            "Earthquake",
            "Ground Deformation",
            "causes"
        )

        self.graph.add_edge(
            "Ground Deformation",
            "Wave Height",
            "generates"
        )

        self.graph.add_edge(
            "Bathymetry",
            "Wave Height",
            "controls"
        )

        self.graph.add_edge(
            "Elevation",
            "Inundation",
            "limits"
        )

        self.graph.add_edge(
            "Wave Height",
            "Inundation",
            "produces"
        )

        self.graph.add_edge(
            "Inundation",
            "Risk",
            "increases"
        )

        self.graph.add_edge(
            "Prediction",
            "DTII",
            "updates"
        )

        self.graph.add_edge(
            "DTII",
            "Risk",
            "estimates"
        )

        return self.graph

    # ---------------------------------------------------------

    def update(
        self,
        node,
        value,
    ):

        self.graph.update_value(
            node,
            value
        )

    # ---------------------------------------------------------

    def get_graph(self):

        return self.graph