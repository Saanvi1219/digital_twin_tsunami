"""
earthquake_model.py

Earthquake source physics.
"""

from math import pow


class EarthquakeModel:

    @staticmethod
    def seismic_moment(magnitude: float) -> float:
        return pow(10, 1.5 * magnitude + 9.1)

    @staticmethod
    def released_energy(magnitude: float) -> float:
        return pow(10, 1.5 * magnitude + 4.8)

    @staticmethod
    def fault_displacement(
        magnitude: float,
        slip: float = 1.0
    ) -> float:
        moment = EarthquakeModel.seismic_moment(magnitude)

        displacement = (
            slip * moment / 1e20
        )

        return max(float(displacement), 0.0)

    @staticmethod
    def source_amplitude(
        magnitude: float,
        slip: float = 1.0
    ) -> float:
        displacement = EarthquakeModel.fault_displacement(
            magnitude,
            slip
        )

        return float(displacement)