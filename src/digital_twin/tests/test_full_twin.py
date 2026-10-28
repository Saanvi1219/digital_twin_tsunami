"""
Full Digital Twin Integration Test
"""

from src.digital_twin.core.twin import DigitalTwin


def run_test():

    print("\n==============================")
    print(" DIGITAL TWIN TEST STARTED ")
    print("==============================\n")


    # --------------------------------
    # 1. Initialize Twin
    # --------------------------------

    twin = DigitalTwin()

    print("✅ Twin Initialized")


    # --------------------------------
    # 2. Load Earthquake
    # --------------------------------

    earthquake = {
    "event": "Sulawesi 2018",
    "latitude": -0.178,
    "longitude": 119.840,
    "depth": 20,
    "magnitude": 7.5
}


    twin.load_earthquake(

        earthquake

    )


    print("✅ Earthquake Loaded")


    # --------------------------------
    # 3. Load DEM
    # --------------------------------
    # import numpy as np
   
    import numpy as np
    dem= np.random.rand(100,100)




    twin.load_dem(

        dem

    )


    print("✅ DEM Loaded")


    # --------------------------------
    # 4. Load Bathymetry
    # --------------------------------
    
    import numpy as np

    bathymetry = np.random.rand(
    100,
    100
)
    twin.load_bathymetry(bathymetry

)


    print("✅ Bathymetry Loaded")


    # --------------------------------
    # 5. Validation
    # --------------------------------

    valid, report = twin.validate()


    print("\nValidation:")
    print(valid)

    print(report)


    # --------------------------------
    # 6. Snapshot
    # --------------------------------

    snapshot = twin.create_snapshot(

        "After Data Loading"

    )


    print("\n✅ Snapshot Created")

    print(snapshot)


    # --------------------------------
    # 7. Summary
    # --------------------------------

    print("\nTwin Summary")

    twin.print_summary()


    # --------------------------------
    # 8. Health
    # --------------------------------

    print("\nHealth Check")

    print(

        twin.health()

    )


    # --------------------------------
    # 9. Statistics
    # --------------------------------

    print("\nEvent Statistics")

    print(

        twin.statistics()

    )


    print("\n==============================")
    print(" DIGITAL TWIN TEST COMPLETE ")
    print("==============================")



if __name__ == "__main__":

    run_test()