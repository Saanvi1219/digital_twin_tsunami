"""
NDWI Processor

Computes the Normalized Difference Water Index (NDWI)
from Sentinel-2 Green and NIR bands.
"""

import numpy as np


class NDWIProcessor:

    # -------------------------------------

    def compute(self, green, nir):

        green = green.astype(np.float32)
        nir = nir.astype(np.float32)

        denominator = green + nir

        denominator[denominator == 0] = 1e-10

        ndwi = (green - nir) / denominator

        return ndwi

    # -------------------------------------

    def water_mask(self, ndwi, threshold=0):

        return (ndwi > threshold).astype(np.uint8)