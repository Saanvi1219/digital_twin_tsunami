"""
Sentinel-1 Loader

Loads Sentinel-1 SAR imagery from GeoTIFF files.
"""

from .raster_loader import RasterLoader


class Sentinel1Loader(RasterLoader):

    def __init__(self, data_dir=None):

        super().__init__(data_dir)

    # --------------------------------------------------

    def download(self):

        raise NotImplementedError(
            "Automatic Sentinel-1 download will be implemented later."
        )

    # --------------------------------------------------

    def load(self, filename):

        return self.read_raster(filename)

    # --------------------------------------------------

    def preprocess(self, filename):

        raster = self.load(filename)

        self.validate(raster)

        return raster

    # --------------------------------------------------

    def validate(self, raster):

        if raster["data"] is None:

            raise ValueError("Sentinel-1 raster is empty.")

        if raster["crs"] is None:

            raise ValueError("CRS missing.")

        return True