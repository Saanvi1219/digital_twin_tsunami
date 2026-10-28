import numpy as np

from src.preprocessing.processors.alignment import RasterAlignment

processor = RasterAlignment()

datasets = {

    "earthquake": {},

    "altimetry": {},

    "dem": {

        "data": np.zeros((100,100))

    },

    "bathymetry": {

        "data": np.zeros((50,60))

    },

    "sentinel1": {

        "data": np.zeros((200,300))

    },

    "sentinel2": {

        "data": np.zeros((400,500))

    }

}

aligned = processor.align_all(datasets)

print()

print("DEM        :", aligned["dem"]["data"].shape)

print("Bathymetry :", aligned["bathymetry"]["data"].shape)

print("Sentinel-1 :", aligned["sentinel1"]["data"].shape)

print("Sentinel-2 :", aligned["sentinel2"]["data"].shape)

print()

print("✓ Alignment Successful")