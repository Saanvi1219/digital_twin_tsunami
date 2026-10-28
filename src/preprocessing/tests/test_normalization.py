import numpy as np

from src.preprocessing.processors.normalization import RasterNormalizer

processor = RasterNormalizer()

datasets = {

    "earthquake": {},

    "altimetry": {},

    "dem": {

        "data": np.random.randint(0,5000,(100,100))

    },

    "bathymetry": {

        "data": np.random.randint(-6000,0,(100,100))

    },

    "sentinel1": {

        "data": np.random.rand(100,100)*40-20

    },

    "sentinel2": {

        "data": np.random.randint(0,10000,(100,100))

    }

}

normalized = processor.normalize_all(datasets)

print()

for key in ["dem","bathymetry","sentinel1","sentinel2"]:

    print(
        key,
        normalized[key]["data"].min(),
        normalized[key]["data"].max()
    )

print()

print("✓ Normalization Successful")