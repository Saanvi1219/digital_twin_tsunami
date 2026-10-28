"""
twin_connector.py

Connects Simulation + DTII
to the Digital Twin.
"""

from src.digital_twin.core.twin import DigitalTwin
from src.digital_twin.integration.simulation_adapter import SimulationAdapter


class TwinConnector:

    def __init__(self):

        self.twin = DigitalTwin()

        # Attach Simulation Engine
        self.twin.attach_simulation_engine(
            SimulationAdapter()
        )

    # =====================================================

    def initialize(
        self,
        features,
    ):
        """
        Load preprocessing outputs
        into the Digital Twin.
        """

        earthquake = {

            "event":
                features.earthquake.event,

            "latitude":
                features.earthquake.latitude,

            "longitude":
                features.earthquake.longitude,

            "depth":
                features.earthquake.depth,

            "magnitude":
                features.earthquake.magnitude,

        }

        self.twin.load_earthquake(
            earthquake
        )

        self.twin.load_dem(
            features.dem
        )

        self.twin.load_bathymetry(
            features.bathymetry
        )

        if features.sentinel1 is not None:

            self.twin.load_sentinel1(
                features.sentinel1
            )

        if features.sentinel2 is not None:

            self.twin.load_sentinel2(
                features.sentinel2
            )

        return self.twin

    # =====================================================

    def update_results(

        self,

        simulation_result,

        dtii_result,

    ):
        """
        Store Simulation + DTII
        inside the Digital Twin.
        """

        self.twin.update(

            simulation=simulation_result,

            dtii=dtii_result,

        )

        self.twin.create_snapshot(

            "Pipeline Update"

        )

        return self.twin

    # =====================================================

    def validate(self):

        return self.twin.validate()

    # =====================================================

    def health(self):

        return self.twin.health()

    # =====================================================

    def summary(self):

        return self.twin.summary()

    # =====================================================

    def get(self):

        return self.twin