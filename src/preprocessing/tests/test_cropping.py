import numpy as np

from src.preprocessing.processors.cropping import RasterCropper

processor = RasterCropper()

datasets = {

    "earthquake": {},

    "altimetry": {},

    "dem": {

        "data": np.zeros((1000,800))

    },

    "bathymetry": {

        "data": np.zeros((700,900))

    },

    "sentinel1": {

        "data": np.zeros((512,512))

    },

    "sentinel2": {

        "data": np.zeros((10980,10980))

    }

}

cropped = processor.crop_all(datasets)

print()

for key in ["dem","bathymetry","sentinel1","sentinel2"]:

    print(key, cropped[key]["data"].shape)

print()

print("✓ Cropping Successful")