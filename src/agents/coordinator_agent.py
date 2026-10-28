"""
coordinator_agent.py

Master Agent

Coordinates the complete Adaptive
Digital Twin workflow.
"""

from src.agents.data_agent import DataAgent
from src.agents.simulation_agent import SimulationAgent
from src.agents.dtii_agent import DTIIAgent
from src.agents.twin_agent import TwinAgent
from src.agents.graph_agent import GraphAgent
from src.agents.llm_agent import LLMAgent


class CoordinatorAgent:

    def __init__(self):

        self.data_agent = DataAgent()

        self.simulation_agent = SimulationAgent()

        self.dtii_agent = DTIIAgent()

        self.twin_agent = TwinAgent()

        self.graph_agent = GraphAgent()
        
        self.llm_agent = LLMAgent()

    # =====================================================

    def execute(

        self,

        earthquake,

        dem,

        bathymetry,

        sentinel1,

        sentinel2,

        altimetry,

    ):

        print("\n====================================")
        print(" MULTI-AGENT TSUNAMI SYSTEM ")
        print("====================================")

        # -------------------------------------------------
        # DATA AGENT
        # -------------------------------------------------

        features = self.data_agent.execute(

            earthquake,

            dem,

            bathymetry,

            sentinel1,

            sentinel2,

            altimetry,

        )

        # -------------------------------------------------
        # SIMULATION AGENT
        # -------------------------------------------------

        simulation = self.simulation_agent.execute(

            features

        )

        # -------------------------------------------------
        # DTII AGENT
        # -------------------------------------------------

        dtii = self.dtii_agent.execute(

            features,

            simulation["summary"],

        )

        # -------------------------------------------------
        # DIGITAL TWIN AGENT
        # -------------------------------------------------

        twin = self.twin_agent.execute(

            features,

            simulation["result"],

            dtii,

        )

        # -------------------------------------------------
        # GRAPH AGENT
        # -------------------------------------------------

        graph = self.graph_agent.execute(

            features,

            simulation["summary"],

            dtii,

        )
        
        llm = self.llm_agent.execute(
            features,
            simulation["summary"],
            dtii,
            twin_state=twin,
        )
            



        print("\n====================================")
        print(" MULTI-AGENT EXECUTION COMPLETED ")
        print("====================================")

        return {

            "features": features,

            "simulation": simulation["result"],

            "summary": simulation["summary"],

            "dtii": dtii,

            "digital_twin": twin,

            "graph": graph,
            
            "llm": llm,

            "health": self.twin_agent.health(),

        }

    # =====================================================

    def system_health(self):

        return self.twin_agent.health()

    # =====================================================

    def twin_summary(self):

        return self.twin_agent.summary()

    # =====================================================

    def graph(self):

        return self.graph_agent.get_graph()