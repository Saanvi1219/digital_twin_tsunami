"""
Simulation Engine Integration Test
"""

import numpy as np

from src.simulation.engine import SimulationEngine
from src.simulation.models import Earthquake


def main():

    print("\n" + "=" * 60)
    print(" TSUNAMI SIMULATION TEST ")
    print("=" * 60)

    # --------------------------------------------------
    # Earthquake
    # --------------------------------------------------

    earthquake = Earthquake(

        event="Sulawesi 2018",

        latitude=-0.178,

        longitude=119.840,

        depth=20,

        magnitude=7.5,

        slip=6.0

    )

    print("✅ Earthquake Created")

    # --------------------------------------------------
    # DEM
    # --------------------------------------------------

    np.random.seed(42)

    dem = np.random.uniform(

        0,

        150,

        (200, 200)

    )

    print("✅ DEM Created")

    # --------------------------------------------------
    # Bathymetry
    # --------------------------------------------------

    bathymetry = np.random.uniform(

        100,

        4000,

        (200, 200)

    )

    print("✅ Bathymetry Created")

    # --------------------------------------------------
    # Engine
    # --------------------------------------------------

    engine = SimulationEngine()

    print("✅ Engine Created")

    # --------------------------------------------------
    # Run
    # --------------------------------------------------

    result = engine.run(

        earthquake,

        dem,

        bathymetry

    )

    print("✅ Simulation Finished")

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    print("\nSimulation Summary\n")

    summary = result.summary()

    for key, value in summary.items():

        print(f"{key:20}: {value}")

    # --------------------------------------------------
    # Assertions
    # --------------------------------------------------

    assert result.successful

    assert result.wave.wave_height.shape == (200, 200)

    assert result.hazard.hazard_map.shape == (200, 200)

    assert result.inundation.inundation_mask.shape == (200, 200)

    print("\n✅ All Assertions Passed")

    print("\n" + "=" * 60)
    print(" SIMULATION TEST PASSED ")
    print("=" * 60)


if __name__ == "__main__":

    main()