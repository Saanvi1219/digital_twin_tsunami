"""
graph_twin.py

Graph representation of the Adaptive Tsunami Digital Twin.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class TwinNode:
    """
    Represents one entity inside the Digital Twin.
    """

    name: str
    value: object
    metadata: Dict = field(default_factory=dict)


class GraphDigitalTwin:
    """
    Stores tsunami entities and their relationships as a graph.
    """

    def __init__(self):

        # Dictionary of node name -> TwinNode
        self.nodes: Dict[str, TwinNode] = {}

        # Adjacency list
        # {
        #   "Earthquake": [
        #       {"target":"Ground Deformation","relation":"causes"},
        #       {"target":"Wave Height","relation":"generates"}
        #   ]
        # }
        self.edges: Dict[str, List[Dict]] = {}

    # -------------------------------------------------------------

    def add_node(
        self,
        name,
        value,
        metadata=None,
    ):

        if metadata is None:
            metadata = {}

        self.nodes[name] = TwinNode(
            name=name,
            value=value,
            metadata=metadata,
        )

        if name not in self.edges:
            self.edges[name] = []

    # -------------------------------------------------------------

    def add_edge(
        self,
        source,
        target,
        relation,
    ):

        if source not in self.nodes:
            raise ValueError(f"Source node '{source}' does not exist.")

        if target not in self.nodes:
            raise ValueError(f"Target node '{target}' does not exist.")

        self.edges[source].append(
            {
                "target": target,
                "relation": relation,
            }
        )

    # -------------------------------------------------------------

    def update_value(
        self,
        node,
        value,
    ):

        if node not in self.nodes:
            raise ValueError(f"{node} not found.")

        self.nodes[node].value = value

    # -------------------------------------------------------------

    def get_value(
        self,
        node,
    ):

        if node not in self.nodes:
            raise ValueError(f"{node} not found.")

        return self.nodes[node].value

    # -------------------------------------------------------------

    def neighbors(
        self,
        node,
    ):

        return self.edges.get(node, [])

    # -------------------------------------------------------------

    def display(self):

        print("\n========== GRAPH DIGITAL TWIN ==========\n")

        for node_name, node in self.nodes.items():

            print(f"{node_name}: {node.value}")

            for edge in self.edges[node_name]:

                print(
                    f"   └──({edge['relation']})──> {edge['target']}"
                )

        print("\n========================================\n")