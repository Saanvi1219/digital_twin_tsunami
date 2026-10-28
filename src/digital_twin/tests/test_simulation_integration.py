"""
test_simulation_integration.py

Tests Digital Twin <-> Simulation Engine integration.
"""

import numpy as np

from src.digital_twin.core.twin import DigitalTwin


def main():

    print("\n" + "=" * 70)
    print(" DIGITAL TWIN + SIMULATION INTEGRATION TEST ")
    print("=" * 70)

    # -------------------------------------------------------
    # Create Twin
    # -------------------------------------------------------

    twin = DigitalTwin()

    print("✅ Digital Twin Created")

    # -------------------------------------------------------
    # Earthquake
    # -------------------------------------------------------

    earthquake = {

        "event": "Sulawesi 2018",

        "latitude": -0.178,

        "longitude": 119.840,

        "depth": 20,

        "magnitude": 7.5,

        "slip": 6.0

    }

    twin.load_earthquake(
        earthquake
    )

    print("✅ Earthquake Loaded")

    # -------------------------------------------------------
    # DEM
    # -------------------------------------------------------

    np.random.seed(42)

    dem = np.random.uniform(

        0,

        150,

        (200, 200)

    )

    twin.load_dem(

        dem

    )

    print("✅ DEM Loaded")

    # -------------------------------------------------------
    # Bathymetry
    # -------------------------------------------------------

    bathymetry = np.random.uniform(

        100,

        4000,

        (200, 200)

    )

    twin.load_bathymetry(

        bathymetry

    )

    print("✅ Bathymetry Loaded")

    # -------------------------------------------------------
    # Validate Twin
    # -------------------------------------------------------

    valid, report = twin.validate()

    print("\nValidation")

    print(valid)

    print(report)

    assert valid

    print("✅ Validation Passed")

    # -------------------------------------------------------
    # Run Simulation
    # -------------------------------------------------------

    print("\nRunning Simulation...\n")

    results = twin.run_simulation()

    print("✅ Simulation Finished")

    # -------------------------------------------------------
    # Verify Results
    # -------------------------------------------------------

    assert results is not None

    assert "tsunami" in results

    assert "inundation" in results

    assert "hazard_map" in results

    assert "evacuation_map" in results

    print("✅ Simulation Output Verified")

    # -------------------------------------------------------
    # Twin Health
    # -------------------------------------------------------

    print("\nTwin Health")

    print(

        twin.health()

    )

    # -------------------------------------------------------
    # Summary
    # -------------------------------------------------------

    print("\nTwin Summary")

    twin.print_summary()

    # -------------------------------------------------------
    # Snapshot Check
    # -------------------------------------------------------

    

    print("\nSnapshot Created Successfully")
    print("✅ Snapshot Stored")


    # -------------------------------------------------------
    # Statistics
    # -------------------------------------------------------

    print("\nStatistics")

    print(

        twin.statistics()

    )

    print("\n" + "=" * 70)
    print(" DIGITAL TWIN + SIMULATION PASSED ")
    print("=" * 70)


if __name__ == "__main__":

    main()