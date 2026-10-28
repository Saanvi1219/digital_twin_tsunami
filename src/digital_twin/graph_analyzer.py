"""
graph_analyzer.py

Analyzes the Graph-Based Digital Twin.
"""

from collections import defaultdict


class GraphAnalyzer:

    def __init__(self, graph):

        self.graph = graph

    # -----------------------------------------------------

    def outgoing_connections(self):

        counts = defaultdict(int)

        for edge in self.graph.edges:
            counts[edge["source"]] += 1

        return dict(counts)

    # -----------------------------------------------------

    def incoming_connections(self):

        counts = defaultdict(int)

        for edge in self.graph.edges:
            counts[edge["target"]] += 1

        return dict(counts)

    # -----------------------------------------------------

    def most_influential_node(self):

        outgoing = self.outgoing_connections()

        if not outgoing:
            return None

        node = max(outgoing, key=outgoing.get)

        return {
            "node": node,
            "connections": outgoing[node]
        }

    # -----------------------------------------------------

    def most_dependent_node(self):

        incoming = self.incoming_connections()

        if not incoming:
            return None

        node = max(incoming, key=incoming.get)

        return {
            "node": node,
            "connections": incoming[node]
        }

    # -----------------------------------------------------

    def isolated_nodes(self):

        connected = set()

        for edge in self.graph.edges:

            connected.add(edge["source"])
            connected.add(edge["target"])

        isolated = []

        for node in self.graph.nodes:

            if node not in connected:
                isolated.append(node)

        return isolated

    # -----------------------------------------------------

    def graph_summary(self):

        return {

            "nodes": len(self.graph.nodes),

            "edges": len(self.graph.edges),

            "most_influential": self.most_influential_node(),

            "most_dependent": self.most_dependent_node(),

            "isolated_nodes": self.isolated_nodes()

        }

    # -----------------------------------------------------

    def explain_graph(self):

        summary = self.graph_summary()

        text = []

        text.append(
            f"Digital Twin contains {summary['nodes']} nodes and {summary['edges']} relationships."
        )

        if summary["most_influential"]:

            info = summary["most_influential"]

            text.append(
                f"{info['node']} influences {info['connections']} other nodes."
            )

        if summary["most_dependent"]:

            info = summary["most_dependent"]

            text.append(
                f"{info['node']} depends on {info['connections']} incoming relationships."
            )

        if summary["isolated_nodes"]:

            text.append(
                "Isolated nodes: "
                + ", ".join(summary["isolated_nodes"])
            )

        return " ".join(text)