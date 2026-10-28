"""
graph_visualizer.py

Visualizes the Graph-Based Digital Twin.
"""

import matplotlib.pyplot as plt
import networkx as nx


class GraphVisualizer:

    def __init__(self, graph):

        self.graph = graph

    # -----------------------------------------------------

    def build_network(self):

        G = nx.DiGraph()

        # ---------------- Nodes ----------------

        for node_name, twin_node in self.graph.nodes.items():

            label = f"{node_name}\n{twin_node.value}"

            G.add_node(
                node_name,
                label=label
            )

        # ---------------- Edges ----------------

        for source, edge_list in self.graph.edges.items():

            for edge in edge_list:

                G.add_edge(
                    source,
                    edge["target"],
                    relation=edge["relation"]
                )

        return G

    # -----------------------------------------------------

    def show(self):

        G = self.build_network()

        pos = nx.spring_layout(
            G,
            seed=42
        )

        plt.figure(figsize=(12, 8))

        nx.draw_networkx_nodes(
            G,
            pos,
            node_size=3000
        )

        nx.draw_networkx_labels(
            G,
            pos,
            labels={
                node: G.nodes[node]["label"]
                for node in G.nodes
            },
            font_size=8
        )

        nx.draw_networkx_edges(
            G,
            pos,
            arrows=True,
            arrowsize=20
        )

        edge_labels = nx.get_edge_attributes(
            G,
            "relation"
        )

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            font_size=8
        )

        plt.title("Graph-Based Digital Twin")

        plt.axis("off")

        plt.tight_layout()

        plt.show()

    # -----------------------------------------------------

    def save(
        self,
        filename="digital_twin_graph.png"
    ):

        G = self.build_network()

        pos = nx.spring_layout(
            G,
            seed=42
        )

        plt.figure(figsize=(12, 8))

        nx.draw_networkx_nodes(
            G,
            pos,
            node_size=3000
        )

        nx.draw_networkx_labels(
            G,
            pos,
            labels={
                node: G.nodes[node]["label"]
                for node in G.nodes
            },
            font_size=8
        )

        nx.draw_networkx_edges(
            G,
            pos,
            arrows=True,
            arrowsize=20
        )

        edge_labels = nx.get_edge_attributes(
            G,
            "relation"
        )

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            font_size=8
        )

        plt.title("Graph-Based Digital Twin")

        plt.axis("off")

        plt.tight_layout()

        plt.savefig(
            filename,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print(f"\nGraph saved as {filename}\n")
