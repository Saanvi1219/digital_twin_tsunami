"""
advanced_graphs.py

Advanced Graph Analytics for the Tsunami Digital Twin.

Generates five research-oriented visualizations:

1. Multi-Agent Interaction Graph
2. Risk Propagation Graph
3. DTII Contribution Graph
4. Validation Metrics Graph
5. Adaptive Digital Twin State Graph
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


class AdvancedGraphSuite:

    def __init__(self, output_dir="outputs/graphs"):

        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # =========================================================
    # 1. MULTI-AGENT INTERACTION GRAPH
    # =========================================================

    def multi_agent_graph(self):

        graph = nx.DiGraph()

        nodes = [

            ("Orchestrator", "orchestrator"),

            ("Data Agent", "agent"),

            ("Observation Agent", "agent"),

            ("Simulation Agent", "agent"),

            ("Validation Agent", "agent"),

            ("DTII Agent", "agent"),

            ("Risk Agent", "agent"),

            ("Adaptive Twin Agent", "agent"),

            ("Graph Agent", "agent"),

            ("LLM Agent", "agent"),

            ("Gemini", "llm"),

        ]

        for node, node_type in nodes:

            graph.add_node(
                node,
                node_type=node_type
            )

        edges = [

            ("Orchestrator", "Data Agent"),
            ("Orchestrator", "Observation Agent"),
            ("Orchestrator", "Simulation Agent"),

            ("Data Agent", "Simulation Agent"),

            ("Observation Agent", "Adaptive Twin Agent"),

            ("Simulation Agent", "Validation Agent"),

            ("Validation Agent", "DTII Agent"),

            ("DTII Agent", "Risk Agent"),

            ("Risk Agent", "Adaptive Twin Agent"),

            ("Adaptive Twin Agent", "Graph Agent"),

            ("Adaptive Twin Agent", "LLM Agent"),

            ("LLM Agent", "Gemini"),

        ]

        graph.add_edges_from(edges)

        plt.figure(figsize=(14, 9))

        position = {

            "Orchestrator": (0, 3),

            "Data Agent": (-3, 2),

            "Observation Agent": (-1, 2),

            "Simulation Agent": (2, 2),

            "Validation Agent": (4, 2),

            "DTII Agent": (4, 0),

            "Risk Agent": (2, -1),

            "Adaptive Twin Agent": (0, -1),

            "Graph Agent": (-2, -2),

            "LLM Agent": (2, -3),

            "Gemini": (4, -4),

        }

        nx.draw_networkx_nodes(
            graph,
            position,
            node_size=2600
        )

        nx.draw_networkx_edges(
            graph,
            position,
            arrows=True,
            arrowsize=18,
            width=1.8
        )

        nx.draw_networkx_labels(
            graph,
            position,
            font_size=9,
            font_weight="bold"
        )

        plt.title(
            "Multi-Agent Tsunami Digital Twin Architecture",
            fontsize=15,
            fontweight="bold"
        )

        plt.axis("off")

        plt.tight_layout()

        path = (
            self.output_dir /
            "multi_agent_interaction.png"
        )

        plt.savefig(
            path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        return path

    # =========================================================
    # 2. RISK PROPAGATION GRAPH
    # =========================================================

    def risk_propagation_graph(
        self,
        features,
        simulation_summary,
        dtii_result,
        risk_result
    ):

        graph = nx.DiGraph()

        earthquake = getattr(
            features.earthquake,
            "magnitude",
            0.0
        )

        wave = simulation_summary.get(
            "max_wave",
            0.0
        )

        flooded_area = simulation_summary.get(
            "flooded_area",
            0.0
        )

        dtii = dtii_result.get(
            "score",
            0.0
        )

        risk = risk_result.get(
            "risk_score",
            0.0
        )

        risk_level = risk_result.get(
            "risk_level",
            "UNKNOWN"
        )

        graph.add_nodes_from([

            (
                "Earthquake",
                {
                    "value":
                        f"M {earthquake:.2f}"
                }
            ),

            (
                "Wave Height",
                {
                    "value":
                        f"{wave:.3f} m"
                }
            ),

            (
                "Inundation",
                {
                    "value":
                        f"{flooded_area:.2f} km²"
                }
            ),

            (
                "DTII",
                {
                    "value":
                        f"{dtii:.4f}"
                }
            ),

            (
                "Risk",
                {
                    "value":
                        f"{risk:.4f}\n{risk_level}"
                }
            ),

        ])

        graph.add_edges_from([

            (
                "Earthquake",
                "Wave Height"
            ),

            (
                "Wave Height",
                "Inundation"
            ),

            (
                "Inundation",
                "Risk"
            ),

            (
                "Wave Height",
                "DTII"
            ),

            (
                "DTII",
                "Risk"
            ),

        ])

        position = {

            "Earthquake": (-2, 2),

            "Wave Height": (0, 2),

            "Inundation": (2, 2),

            "DTII": (0, 0),

            "Risk": (2, 0),

        }

        plt.figure(figsize=(12, 7))

        nx.draw_networkx_nodes(
            graph,
            position,
            node_size=3000
        )

        nx.draw_networkx_edges(
            graph,
            position,
            arrows=True,
            arrowsize=20,
            width=2
        )

        labels = {}

        for node, data in graph.nodes(data=True):

            labels[node] = (
                f"{node}\n"
                f"{data['value']}"
            )

        nx.draw_networkx_labels(
            graph,
            position,
            labels=labels,
            font_size=9,
            font_weight="bold"
        )

        plt.title(
            "Tsunami Risk Propagation",
            fontsize=15,
            fontweight="bold"
        )

        plt.axis("off")

        plt.tight_layout()

        path = (
            self.output_dir /
            "risk_propagation.png"
        )

        plt.savefig(
            path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        return path

    # =========================================================
    # 3. DTII CONTRIBUTION GRAPH
    # =========================================================

    def dtii_contribution_graph(
        self,
        dtii_result
    ):

        features = dtii_result.get(
            "features",
            {}
        )

        # These are the actual DTII weights
        # used by the current scorer.

        weights = {

            "seismic": 0.20,

            "deformation": 0.20,

            "elevation": 0.15,

            "wave": 0.20,

            "inundation": 0.15,

            "prediction": 0.10,

        }

        names = []

        contributions = []

        for feature, weight in weights.items():

            value = float(
                features.get(
                    feature,
                    0.0
                )
            )

            contribution = (
                value * weight
            )

            names.append(
                feature.capitalize()
            )

            contributions.append(
                contribution
            )

        plt.figure(figsize=(11, 6))

        bars = plt.barh(
            names,
            contributions
        )

        plt.xlabel(
            "Weighted contribution to DTII"
        )

        plt.ylabel(
            "DTII component"
        )

        plt.title(
            "DTII Component Contributions",
            fontsize=15,
            fontweight="bold"
        )

        plt.grid(
            axis="x",
            alpha=0.25
        )

        for bar, value in zip(
            bars,
            contributions
        ):

            plt.text(
                value + 0.005,
                bar.get_y()
                + bar.get_height() / 2,
                f"{value:.4f}",
                va="center"
            )

        plt.tight_layout()

        path = (
            self.output_dir /
            "dtii_contribution.png"
        )

        plt.savefig(
            path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        return path

    # =========================================================
    # 4. VALIDATION METRICS GRAPH
    # =========================================================

    def validation_metrics_graph(
        self,
        validation_result
    ):

        metrics = {

            "F1": validation_result.get(
                "f1_score",
                0.0
            ),

            "IoU": validation_result.get(
                "iou",
                0.0
            ),

            "Precision": validation_result.get(
                "precision",
                0.0
            ),

            "Recall": validation_result.get(
                "recall",
                0.0
            ),

            "Confidence": validation_result.get(
                "confidence",
                0.0
            ),

        }

        names = list(
            metrics.keys()
        )

        values = list(
            metrics.values()
        )

        plt.figure(figsize=(11, 6))

        bars = plt.bar(
            names,
            values
        )

        plt.ylim(
            0,
            1.05
        )

        plt.ylabel(
            "Score"
        )

        plt.title(
            "Tsunami Model Validation Performance",
            fontsize=15,
            fontweight="bold"
        )

        plt.grid(
            axis="y",
            alpha=0.25
        )

        for bar, value in zip(
            bars,
            values
        ):

            plt.text(
                bar.get_x()
                + bar.get_width() / 2,
                value + 0.02,
                f"{value:.3f}",
                ha="center"
            )

        plt.tight_layout()

        path = (
            self.output_dir /
            "validation_metrics.png"
        )

        plt.savefig(
            path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        return path

    # =========================================================
    # 5. ADAPTIVE DIGITAL TWIN STATE GRAPH
    # =========================================================

    def adaptive_twin_state_graph(
        self,
        observation_result,
        twin_summary
    ):

        change_score = float(
            observation_result.get(
                "change_score",
                0.0
            )
        )

        adaptation_required = bool(
            observation_result.get(
                "adaptation_required",
                False
            )
        )

        changed = bool(
            observation_result.get(
                "changed",
                False
            )
        )

        anomaly = bool(
            observation_result.get(
                "anomaly",
                False
            )
        )

        version = twin_summary.get(
            "version",
            1
        )

        history = twin_summary.get(
            "history",
            0
        )

        events = twin_summary.get(
            "events",
            0
        )

        graph = nx.DiGraph()

        graph.add_nodes_from([

            (
                "Observation",
                {
                    "value":
                        f"Change={change_score:.3f}"
                }
            ),

            (
                "Change Detection",
                {
                    "value":
                        f"Changed={changed}"
                }
            ),

            (
                "Anomaly Detection",
                {
                    "value":
                        f"Anomaly={anomaly}"
                }
            ),

            (
                "Adaptation Decision",
                {
                    "value":
                        (
                            "ADAPT"
                            if adaptation_required
                            else
                            "NO ADAPTATION"
                        )
                }
            ),

            (
                "Digital Twin",
                {
                    "value":
                        f"Version {version}"
                }
            ),

            (
                "History",
                {
                    "value":
                        f"{history} snapshots"
                }
            ),

            (
                "Events",
                {
                    "value":
                        f"{events} events"
                }
            ),

        ])

        graph.add_edges_from([

            (
                "Observation",
                "Change Detection"
            ),

            (
                "Observation",
                "Anomaly Detection"
            ),

            (
                "Change Detection",
                "Adaptation Decision"
            ),

            (
                "Anomaly Detection",
                "Adaptation Decision"
            ),

            (
                "Adaptation Decision",
                "Digital Twin"
            ),

            (
                "Digital Twin",
                "History"
            ),

            (
                "Digital Twin",
                "Events"
            ),

        ])

        position = {

            "Observation": (-3, 1),

            "Change Detection": (-1, 2),

            "Anomaly Detection": (-1, 0),

            "Adaptation Decision": (1, 1),

            "Digital Twin": (3, 1),

            "History": (3, 2.5),

            "Events": (3, -0.5),

        }

        plt.figure(figsize=(13, 7))

        nx.draw_networkx_nodes(
            graph,
            position,
            node_size=2600
        )

        nx.draw_networkx_edges(
            graph,
            position,
            arrows=True,
            arrowsize=18,
            width=1.8
        )

        labels = {}

        for node, data in graph.nodes(data=True):

            labels[node] = (
                f"{node}\n"
                f"{data['value']}"
            )

        nx.draw_networkx_labels(
            graph,
            position,
            labels=labels,
            font_size=8,
            font_weight="bold"
        )

        plt.title(
            "Adaptive Digital Twin State Evolution",
            fontsize=15,
            fontweight="bold"
        )

        plt.axis("off")

        plt.tight_layout()

        path = (
            self.output_dir /
            "adaptive_twin_state.png"
        )

        plt.savefig(
            path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        return path

    # =========================================================
    # GENERATE ALL FIVE
    # =========================================================

    def generate_all(
        self,
        features,
        simulation_summary,
        dtii_result,
        risk_result,
        validation_result,
        observation_result,
        twin_summary
    ):

        generated = {}

        generated[
            "multi_agent"
        ] = self.multi_agent_graph()

        generated[
            "risk_propagation"
        ] = self.risk_propagation_graph(
            features,
            simulation_summary,
            dtii_result,
            risk_result
        )

        generated[
            "dtii_contribution"
        ] = self.dtii_contribution_graph(
            dtii_result
        )

        generated[
            "validation"
        ] = self.validation_metrics_graph(
            validation_result
        )

        generated[
            "adaptive_twin"
        ] = self.adaptive_twin_state_graph(
            observation_result,
            twin_summary
        )

        print(
            "\n[GRAPH SUITE] "
            "Advanced graphs generated:"
        )

        for name, path in generated.items():

            print(
                f"  ✓ {name}: {path}"
            )

        return generated