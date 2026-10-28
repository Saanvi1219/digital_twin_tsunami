"""
pipeline.py

Complete Adaptive Digital Twin Pipeline
"""

from src.preprocessing.pipeline import PreprocessingPipeline

from src.integration.data_adapter import DataAdapter

from src.integration.simulation_connector import SimulationConnector

from src.integration.dtii_connector import DTIIConnector

from src.integration.twin_connector import TwinConnector

from src.digital_twin.graph_builder import GraphBuilder


class TsunamiPipeline:

    def __init__(self):

        self.preprocessing = PreprocessingPipeline()

        self.adapter = DataAdapter()

        self.simulation = SimulationConnector()

        self.dtii = DTIIConnector()

        self.twin = TwinConnector()

        self.graph = GraphBuilder()
        

    # =====================================================

    def run(

        self,

        earthquake,

        dem,

        bathymetry,

        sentinel1,

        sentinel2,

        altimetry,

    ):

        print("\n==============================")

        print(" PREPROCESSING ")

        print("==============================")

        datasets = self.preprocessing.run(

            earthquake,

            dem,

            bathymetry,

            sentinel1,

            sentinel2,

            altimetry,

        )

        print("\n==============================")

        print(" ADAPTER ")

        print("==============================")

        features = self.adapter.adapt(

            datasets

        )

        print("\n==============================")

        print(" SIMULATION ")

        print("==============================")

        simulation = self.simulation.run(

            features

        )

        simulation_summary = self.simulation.summary()

        print(simulation_summary)

        print("\n==============================")

        print(" DTII ")

        print("==============================")

        dtii = self.dtii.compute(

            features,

            simulation_summary,

        )

        self.dtii.summary(

            dtii

        )

        print("\n==============================")

        print(" DIGITAL TWIN ")

        print("==============================")

        twin = self.twin.initialize(

            features

        )

        self.twin.update_results(

            simulation_summary,

            dtii,

        )

        print(

            self.twin.summary()

        )

        print("\n==============================")

        print(" GRAPH ")

        print("==============================")

        graph = self.graph.build(

            magnitude=features.earthquake.magnitude,

            deformation=features.ground_deformation,

            elevation=features.mean_elevation,

            bathymetry=features.mean_bathymetry,

            wave_height=simulation_summary["max_wave"],

            inundation=simulation_summary["flooded_area"],

            prediction=1.0,

            dtii_score=dtii["score"],

            risk_level=dtii["level"],

        )
        
        

        print("\n")
        
        
        



        print("PIPELINE COMPLETED")

        print()

        return {

            "features": features,

            "simulation": simulation,

            "summary": simulation_summary,

            "dtii": dtii,

            "twin": twin,

            "graph": graph,
            

            
            "twin_health": self.twin.health(),

        }