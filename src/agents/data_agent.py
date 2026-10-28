"""
data_agent.py

Responsible for:
- Running preprocessing
- Converting raw datasets into TsunamiFeatures
"""

from src.preprocessing.pipeline import PreprocessingPipeline
from src.integration.data_adapter import DataAdapter


class DataAgent:

    def __init__(self):

        self.pipeline = PreprocessingPipeline()

        self.adapter = DataAdapter()

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

        print("\n[DATA AGENT] Running preprocessing...")

        datasets = self.pipeline.run(

            earthquake,

            dem,

            bathymetry,

            sentinel1,

            sentinel2,

            altimetry,

        )

        print("[DATA AGENT] Converting datasets...")

        features = self.adapter.adapt(

            datasets

        )

        print("[DATA AGENT] Completed.")

        return features