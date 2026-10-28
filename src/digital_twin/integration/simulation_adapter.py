"""
simulation_adapter.py

Connects Digital Twin with Simulation Engine.
"""


from src.simulation.engine import SimulationEngine
from src.simulation.models import Earthquake



class SimulationAdapter:
    """
    Adapter between Digital Twin and Simulation Engine.
    """


    def __init__(self):

        self.engine = SimulationEngine()



    def run(self, state):
        """
        Convert TwinState into simulation input.
        """


        earthquake = Earthquake(

            event=state.earthquake["event"],

            latitude=state.earthquake["latitude"],

            longitude=state.earthquake["longitude"],

            depth=state.earthquake["depth"],

            magnitude=state.earthquake["magnitude"],

        )


        result = self.engine.run(

            earthquake,

            state.dem,

            state.bathymetry

        )


        return {

            "tsunami":

                result.wave.wave_height,


            "inundation":

                result.inundation.inundation_mask,


            "hazard_map":

                result.hazard.hazard_map,


            "evacuation_map":

                result.hazard.evacuation_time,


            "simulation_result":

                result

        }