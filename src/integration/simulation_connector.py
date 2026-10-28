"""
simulation_connector.py

Connects preprocessing outputs to the
Simulation Engine.
"""

from src.simulation.engine import SimulationEngine

from .data_adapter import TsunamiFeatures


class SimulationConnector:
    """
    Runs the tsunami simulation using
    features extracted from preprocessing.
    """

    def __init__(self):

        self.engine = SimulationEngine()

    # =====================================================

    def run(

        self,

        features: TsunamiFeatures,

    ):

        """
        Execute tsunami simulation.
        """

        result = self.engine.run(

            earthquake=features.earthquake,

            dem=features.dem,

            bathymetry=features.bathymetry,

            dem_transform=features.dem_transform,

        )

        return result

    # =====================================================

    def summary(self):

        """
        Return summary of latest simulation.
        """

        return self.engine.summary()

    # =====================================================

    @property
    def last_result(self):

        return self.engine.last_result