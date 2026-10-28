"""
orchestrator_agent.py

Adaptive Multi-Agent Orchestrator
----------------------------------

Controls the complete tsunami Digital Twin lifecycle.

Agents:
    Observation
    Data
    Simulation
    DTII
    Adaptive Twin
    Validation
    Risk
    Graph

The Orchestrator decides when the Digital Twin
needs to adapt or simulation needs to be rerun.
"""

from __future__ import annotations

from typing import Any, Dict

from src.agents.data_agent import DataAgent
from src.agents.simulation_agent import SimulationAgent
from src.agents.dtii_agent import DTIIAgent
from src.agents.graph_agent import GraphAgent

from src.agents.observation_agent import ObservationAgent
from src.agents.adaptive_twin_agent import AdaptiveTwinAgent
from src.agents.validation_agent import ValidationAgent
from src.agents.risk_agent import RiskAgent
from src.agents.llm_agent import LLMAgent


class OrchestratorAgent:

    def __init__(self):

        print(
            "\n[ORCHESTRATOR] "
            "Initializing multi-agent system..."
        )

        # -------------------------------------------------
        # Existing agents
        # -------------------------------------------------

        self.data_agent = DataAgent()

        self.simulation_agent = (
            SimulationAgent()
        )

        self.dtii_agent = (
            DTIIAgent()
        )

        self.graph_agent = (
            GraphAgent()
        )

        # -------------------------------------------------
        # New adaptive agents
        # -------------------------------------------------

        self.observation_agent = (
            ObservationAgent()
        )

        self.adaptive_twin_agent = (
            AdaptiveTwinAgent()
        )

        self.validation_agent = (
            ValidationAgent()
        )

        self.risk_agent = (
            RiskAgent()
        )
        
        self.llm_agent = None

        # -------------------------------------------------

        self.execution_count = 0

        self.last_results = None

    # =====================================================
    # MAIN EXECUTION
    # =====================================================

    def execute(

        self,

        earthquake,

        dem,

        bathymetry,

        sentinel1,

        sentinel2,

        altimetry,

    ) -> Dict[str, Any]:

        self.execution_count += 1

        print("\n")
        print("=" * 70)
        print(" ADAPTIVE MULTI-AGENT TSUNAMI DIGITAL TWIN ")
        print("=" * 70)

        # =================================================
        # STEP 1
        # DATA AGENT
        # =================================================

        print("\n[ORCHESTRATOR] STEP 1: Data ingestion")

        features = self.data_agent.execute(

            earthquake,

            dem,

            bathymetry,

            sentinel1,

            sentinel2,

            altimetry,

        )

        # =================================================
        # STEP 2
        # OBSERVATION AGENT
        # =================================================

        print(
            "\n[ORCHESTRATOR] "
            "STEP 2: Observation analysis"
        )

        observation = (
            self.observation_agent.execute(
                features
            )
        )

        # =================================================
        # STEP 3
        # ADAPTIVE TWIN DECISION
        # =================================================

        print(
            "\n[ORCHESTRATOR] "
            "STEP 3: Adaptive Twin decision"
        )

        adaptation = (
            self.adaptive_twin_agent
            .update_from_observation(
                observation
            )
        )

        # =================================================
        # STEP 4
        # SIMULATION
        # =================================================

        print(
            "\n[ORCHESTRATOR] "
            "STEP 4: Tsunami simulation"
        )

        # For the first execution simulation is mandatory.
        #
        # For later executions, observation changes
        # determine whether a new simulation is required.

        run_simulation = (

            self.execution_count == 1

            or

            adaptation[
                "adaptation_required"
            ]

        )

        if run_simulation:

            simulation = (
                self.simulation_agent.execute(
                    features
                )
            )

            simulation_result = (
                simulation["result"]
            )

            simulation_summary = (
                simulation["summary"]
            )

        else:

            print(
                "[ORCHESTRATOR] "
                "No significant observation change."
            )

            print(
                "[ORCHESTRATOR] "
                "Using previous simulation."
            )

            simulation_result = (
                self.simulation_agent.last_result()
            )

            simulation_summary = (
                self.simulation_agent.summary()
            )

            simulation = {

                "result":
                    simulation_result,

                "summary":
                    simulation_summary,

                "reused":
                    True,

            }

        # =================================================
        # STEP 5
        # VALIDATION
        # =================================================

        print(
            "\n[ORCHESTRATOR] "
            "STEP 5: Model validation"
        )

        validation = (
            self.validation_agent.execute(

                simulation_result,

                features,

            )
        )

        # =================================================
        # STEP 6
        # DTII
        # =================================================

        print(
            "\n[ORCHESTRATOR] "
            "STEP 6: DTII calculation"
        )

        prediction_confidence = (
            validation.get(
                "confidence",
                1.0
            )
        )

        dtii = self.dtii_agent.execute(

            features,

            simulation_summary,

            prediction_confidence,

        )

        # =================================================
        # STEP 7
        # RISK
        # =================================================

        print(
            "\n[ORCHESTRATOR] "
            "STEP 7: Risk assessment"
        )

        risk = self.risk_agent.execute(

            dtii,

            simulation_result,

            validation,

            observation,

        )

        # =================================================
        # STEP 8
        # ADAPTIVE DIGITAL TWIN UPDATE
        # =================================================

        print(
            "\n[ORCHESTRATOR] "
            "STEP 8: Digital Twin adaptation"
        )

        twin = (
            self.adaptive_twin_agent.update(

                simulation_result,

                dtii,

                validation,
                
                features=features,

            )
        )

        # =================================================
        # STEP 9
        # GRAPH DIGITAL TWIN
        # =================================================

        print(
            "\n[ORCHESTRATOR] "
            "STEP 9: Graph Digital Twin"
        )

        graph = self.graph_agent.execute(

            features,

            simulation_summary,

            dtii,

        )
        
        
        # =================================================
# STEP 10
# LLM DECISION INTELLIGENCE
# =================================================

        print(
            "\n[ORCHESTRATOR] "
            "STEP 10: LLM Decision Intelligence"
        )
        llm = {
            "enabled":  False,
            "status": "skipped",
        }
        
    
            

        # =================================================
        # STEP 10
        # HEALTH
        # =================================================

        health = (
            self.adaptive_twin_agent.health()
        )

        # =================================================
        # FINAL RESULT
        # =================================================

        results = {

            "features":
                features,

            "observation":
                observation,

            "adaptation":
                adaptation,

            "simulation":
                simulation_result,

            "summary":
                simulation_summary,

            "validation":
                validation,

            "dtii":
                dtii,

            "risk":
                risk,

            "digital_twin":
                twin,

            "graph":
                graph,

            "health":
                health,
                
            "llm":
                llm,

            "execution":
                {

                    "count":
                        self.execution_count,

                    "simulation_rerun":
                        run_simulation,

                }

        }

        self.last_results = results

        print("\n")
        print("=" * 70)
        print(" ADAPTIVE MULTI-AGENT EXECUTION COMPLETED ")
        print("=" * 70)

        print(
            "\nRisk:",
            risk["risk_level"]
        )

        print(
            "Risk Score:",
            round(
                risk["risk_score"],
                4
            )
        )

        print(
            "Validation Confidence:",
            round(
                validation.get(
                    "confidence",
                    0.0
                ),
                4
            )
        )

        print(
            "Simulation Rerun:",
            run_simulation
        )

        print("=" * 70)

        return results

    # =====================================================
    # SYSTEM HEALTH
    # =====================================================

    def system_health(self):

        return (
            self.adaptive_twin_agent.health()
        )

    # =====================================================
    # LAST RESULTS
    # =====================================================

    def last_results(self):

        return self.last_results