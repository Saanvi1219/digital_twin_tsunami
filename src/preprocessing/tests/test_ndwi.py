import numpy as np

from src.preprocessing.processors.ndwi import NDWIProcessor

processor = NDWIProcessor()

green = np.random.randint(
    100,
    2000,
    (256,256)
)

nir = np.random.randint(
    100,
    2000,
    (256,256)
)

ndwi = processor.compute(green, nir)

mask = processor.water_mask(ndwi)

print()

print("NDWI Shape :", ndwi.shape)

print("Minimum    :", ndwi.min())

print("Maximum    :", ndwi.max())

print("Water Pixels:", mask.sum())

print()

print("✓ NDWI Processor Working")